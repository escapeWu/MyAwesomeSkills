#!/usr/bin/env python3
"""Adaptive Perplexity web/deep research via HTTP chat completions endpoint."""

from __future__ import annotations

import argparse
import codecs
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"
CONFIG_EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "config.example.json"
DEFAULT_BASE_URL = "https://api.perplexity.ai"
DEFAULT_FAST_MODEL = "sonar"
DEFAULT_MODEL = "sonar-pro"
DEFAULT_EXPERT_MODEL = "sonar-deep-research"
DEFAULT_MODE = "auto"
MAX_STAGE_NOTE_CHARS = 6000
DEFAULT_TECH_REQUIRED_SOURCES = ["Reddit", "Hacker News"]

SYSTEM_PROMPT = (
    "You are a fast Perplexity-powered web research assistant. "
    "Prioritize current, reliable web evidence. "
    "Answer concisely and include source URLs in a final Sources section."
)

SCOUT_SYSTEM_PROMPT = (
    "You are a stage-1 web scout. Work quickly. "
    "Identify hard facts, useful sub-questions, and remaining gaps. "
    "Always include source URLs."
)

EXPERT_SYSTEM_PROMPT = (
    "You are a stage-2 expert web research synthesizer. "
    "Use prior notes as hints, then re-check important claims with web evidence. "
    "Return a structured, high-signal final answer with source URLs."
)

COMPLEX_KEYWORDS = [
    "compare", "comparison", "vs", "versus", "tradeoff", "analyze", "analysis",
    "investigate", "investigation", "audit", "deep", "research", "timeline",
    "cross-check", "verify", "contradiction", "root cause", "synthesize",
    "评估", "分析", "比较", "对比", "调研", "调查", "深度", "审计", "时间线", "影响", "原因", "矛盾", "交叉验证", "拆解",
]

SIMPLE_HINTS = ["latest", "today", "current", "news", "price", "weather", "what is", "谁是", "是什么", "最新", "刚刚", "价格", "行情"]

TECHNICAL_QUERY_KEYWORDS = [
    "api", "sdk", "bug", "error", "exception", "stack trace", "github", "python", "javascript",
    "typescript", "node", "react", "vue", "next.js", "docker", "kubernetes", "postgres", "redis",
    "linux", "macos", "llm", "model", "benchmark", "framework", "library", "dependency", "release", "changelog",
    "性能", "报错", "错误", "异常", "版本", "兼容", "依赖", "框架", "库", "接口", "源码", "部署", "容器", "数据库", "前端", "后端", "模型", "基准",
]


def load_config() -> dict[str, Any]:
    path = CONFIG_PATH if CONFIG_PATH.exists() else CONFIG_EXAMPLE_PATH
    if not path.exists():
        raise RuntimeError(f"Missing config file: {CONFIG_PATH} (or {CONFIG_EXAMPLE_PATH})")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid config format: {path}")
    return data


def extract_urls(text: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for match in re.findall(r"https?://[^\s)\]>\"']+", text or ""):
        clean = match.rstrip('.,;')
        if clean not in seen:
            seen.add(clean)
            urls.append(clean)
    return urls


def extract_payload_urls(payload: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(payload, dict):
        for key in ("citations", "search_results"):
            value = payload.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        urls.extend(extract_urls(item))
                    elif isinstance(item, dict):
                        for url_key in ("url", "link", "source", "citation"):
                            if item.get(url_key):
                                urls.extend(extract_urls(str(item[url_key])))
        for value in payload.values():
            if isinstance(value, (dict, list)):
                urls.extend(extract_payload_urls(value))
    elif isinstance(payload, list):
        for item in payload:
            urls.extend(extract_payload_urls(item))
    return dedupe_keep_order(urls)


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            output.append(item)
    return output


def truncate_text(text: str, limit: int = MAX_STAGE_NOTE_CHARS) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "\n\n[truncated]"


def is_technical_query(query: str) -> bool:
    q = query or ""
    lower = q.lower()
    if any(keyword in lower or keyword in q for keyword in TECHNICAL_QUERY_KEYWORDS):
        return True
    return bool(re.search(r"\b[A-Za-z0-9_.+-]+(?:\.js|\.py|\.ts|\.tsx|\.jsx|\.go|\.rs|\.java|\.yaml|\.yml|\.json)\b", q))


def get_technical_required_sources(config: dict[str, Any]) -> list[str]:
    raw_sources = config.get("technical_required_sources", DEFAULT_TECH_REQUIRED_SOURCES)
    if isinstance(raw_sources, str):
        sources = [part.strip() for part in raw_sources.split(",")]
    elif isinstance(raw_sources, list):
        sources = [str(part).strip() for part in raw_sources]
    else:
        sources = DEFAULT_TECH_REQUIRED_SOURCES
    return [source for source in sources if source]


def build_source_requirement_note(query: str, required_sources: list[str] | None = None) -> str:
    if not required_sources or not is_technical_query(query):
        return ""
    domains: list[str] = []
    for source in required_sources:
        normalized = source.lower().replace(" ", "")
        if normalized in {"reddit", "r/reddit"}:
            domains.append("reddit.com")
        elif normalized in {"hackernews", "hn"}:
            domains.append("news.ycombinator.com")
    domain_text = f" ({', '.join(dedupe_keep_order(domains))})" if domains else ""
    return (
        "\n\nTechnical-source requirement: This is a technical query. "
        f"You MUST include search coverage from {' and '.join(required_sources)}{domain_text} in addition to official docs, GitHub, or vendor sources when relevant. "
        "If one of these communities has no relevant/current result, explicitly say so instead of silently omitting it."
    )


def extract_choice_text(choice: dict[str, Any]) -> tuple[str, str]:
    delta = choice.get("delta") or {}
    message = choice.get("message") or {}
    reasoning = delta.get("reasoning_content") or message.get("reasoning_content") or ""
    content = delta.get("content")
    if content is None:
        content = message.get("content", "")
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("content") or ""))
            elif item:
                parts.append(str(item))
        content = "".join(parts)
    elif not isinstance(content, str):
        content = str(content or "")
    return str(reasoning), str(content)


def parse_sse_response(response: requests.Response) -> tuple[str, str, list[dict[str, Any]]]:
    reasoning_parts: list[str] = []
    content_parts: list[str] = []
    chunks: list[dict[str, Any]] = []
    decoder = json.JSONDecoder()
    utf8_decoder = codecs.getincrementaldecoder("utf-8")()
    text_buffer = ""
    for raw in response.iter_content(chunk_size=1024):
        if not raw:
            continue
        text_buffer += utf8_decoder.decode(raw)
        while "\n\n" in text_buffer:
            event, text_buffer = text_buffer.split("\n\n", 1)
            for line in event.splitlines():
                line = line.strip()
                if not line.startswith("data:"):
                    continue
                data_str = line[5:].strip()
                if not data_str or data_str == "[DONE]":
                    continue
                chunk, end = decoder.raw_decode(data_str)
                if data_str[end:].strip():
                    raise RuntimeError(f"Unexpected extra data after SSE JSON: {data_str[end:][:200]!r}")
                if isinstance(chunk, dict):
                    chunks.append(chunk)
                    for choice in chunk.get("choices", []):
                        reasoning, content = extract_choice_text(choice)
                        if reasoning:
                            reasoning_parts.append(reasoning)
                        if content:
                            content_parts.append(content)
    tail = utf8_decoder.decode(b"", final=True)
    if tail:
        text_buffer += tail
    return "".join(reasoning_parts).strip(), "".join(content_parts).strip(), chunks


def parse_json_response(response: requests.Response) -> tuple[str, str, list[dict[str, Any]]]:
    payload = response.json()
    reasoning_parts: list[str] = []
    content_parts: list[str] = []
    for choice in payload.get("choices", []):
        reasoning, content = extract_choice_text(choice)
        if reasoning:
            reasoning_parts.append(reasoning)
        if content:
            content_parts.append(content)
    return "".join(reasoning_parts).strip(), "".join(content_parts).strip(), [payload]


def post_chat_completion(messages: list[dict[str, str]], model: str, base_url: str, api_key: str, temperature: float = 0.2, stream: bool = False, timeout: int = 240, extra_body: dict[str, Any] | None = None) -> tuple[str, str, list[dict[str, Any]]]:
    if not api_key or api_key in {"REPLACE_ME", "***"}:
        raise RuntimeError(f"Missing api_key in {CONFIG_PATH}. Copy config.example.json to config.json and set a Perplexity API key.")
    url = base_url.rstrip("/") + "/chat/completions"
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": stream,
    }
    if extra_body:
        payload.update(extra_body)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream, application/json",
    }
    with requests.post(url, headers=headers, json=payload, timeout=timeout, stream=stream) as response:
        response.raise_for_status()
        content_type = (response.headers.get("content-type") or "").lower()
        if stream or "text/event-stream" in content_type:
            return parse_sse_response(response)
        if "application/json" in content_type:
            return parse_json_response(response)
        raise RuntimeError(f"Unsupported response content-type={content_type!r}")


def build_single_user_prompt(query: str, max_sources: int, language: str, required_sources: list[str] | None = None) -> str:
    return (
        f"User query: {query}\n\n"
        "Find current, relevant information from the web. "
        "Return the concise answer first, then a 'Sources:' section with numbered source URLs. "
        f"Limit the sources section to at most {max_sources} URLs. Reply in {language}."
        f"{build_source_requirement_note(query, required_sources)}"
    )


def build_scout_prompt(query: str, max_sources: int, language: str, required_sources: list[str] | None = None) -> str:
    return (
        f"Original task: {query}\n\n"
        "Do a fast scouting pass. Break the task into useful sub-questions, collect hard facts, and note gaps.\n\n"
        "Return exactly these sections:\nSummary:\nClaims to verify:\nKey gaps:\nSources:\n"
        f"Keep it compact. Limit Sources to at most {max_sources} URLs. Reply in {language}."
        f"{build_source_requirement_note(query, required_sources)}"
    )


def build_gap_fill_prompt(query: str, scout_notes: str, gaps: list[str], max_sources: int, language: str, required_sources: list[str] | None = None) -> str:
    gap_text = "\n".join(f"- {gap}" for gap in gaps[:6]) or "- No explicit gaps extracted; focus on weakly supported claims."
    return (
        f"Original task: {query}\n\nStage-1 scout notes:\n{truncate_text(scout_notes, 3000)}\n\n"
        f"Focus ONLY on unresolved gaps below:\n{gap_text}\n\n"
        "Return exactly these sections:\nGap findings:\nWhat is now resolved:\nRemaining uncertainty:\nSources:\n"
        f"Limit Sources to at most {max_sources} URLs. Reply in {language}."
        f"{build_source_requirement_note(query, required_sources)}"
    )


def build_expert_prompt(query: str, scout_notes: str, gap_notes: str | None, max_sources: int, language: str, required_sources: list[str] | None = None) -> str:
    sections = [f"Original task: {query}", "", "Stage-1 scout notes:", truncate_text(scout_notes)]
    if gap_notes:
        sections.extend(["", "Gap-fill notes:", truncate_text(gap_notes)])
    sections.extend([
        "", "Now produce the final answer.",
        "Re-check important claims with fresh web evidence rather than blindly trusting the notes above.",
        "Return a concise but complete answer first, then a 'Sources:' section with numbered URLs.",
        f"Limit Sources to at most {max_sources} URLs.", f"Reply in {language}.", build_source_requirement_note(query, required_sources),
    ])
    return "\n".join(sections)


def extract_gap_candidates(text: str) -> list[str]:
    match = re.search(r"(?:Key gaps|Gaps|Missing information|Remaining uncertainty)\s*:\s*(.*?)(?:\n(?:Sources|Gap findings|What is now resolved|Summary|Claims to verify)\s*:|\Z)", text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    items: list[str] = []
    for line in match.group(1).strip().splitlines():
        cleaned = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", line).strip()
        if cleaned and cleaned.lower() not in {"none", "n/a", "无", "暂无"}:
            items.append(cleaned)
    return items[:6]


def assess_complexity(query: str) -> dict[str, Any]:
    q = (query or "").strip()
    lower = q.lower()
    score = 0
    reasons: list[str] = []
    if len(q) > 140:
        score += 2; reasons.append("query is fairly long")
    if len(q) > 280:
        score += 1; reasons.append("query is very long")
    keyword_hits = [kw for kw in COMPLEX_KEYWORDS if kw in lower or kw in q]
    if keyword_hits:
        score += min(4, len(keyword_hits)); reasons.append("contains analytical / investigative language")
    if len(re.findall(r"[?？]", q)) >= 2:
        score += 1; reasons.append("contains multiple explicit questions")
    separators = [",", "，", ";", "；", " and ", "以及", "同时", "并且"]
    if sum(1 for sep in separators if sep in lower or sep in q) >= 2:
        score += 1; reasons.append("asks for multiple dimensions or sub-parts")
    if any(token in lower or token in q for token in ["source", "sources", "with links", "引用", "来源", "证据"]):
        score += 1; reasons.append("explicitly asks for sources / evidence")
    simple_hits = [kw for kw in SIMPLE_HINTS if kw in lower or kw in q]
    if simple_hits and len(q) < 90 and not keyword_hits:
        score -= 1; reasons.append("looks like a short freshness-sensitive lookup")
    label = "simple" if score <= 1 else "standard" if score <= 4 else "complex"
    return {"complexity": label, "complexity_score": max(score, 0), "reasons": reasons or ["default routing"], "keyword_hits": keyword_hits[:8]}


def resolve_models(config: dict[str, Any]) -> dict[str, str]:
    balanced = config.get("auto_model") or config.get("model") or DEFAULT_MODEL
    return {"fast": config.get("fast_model") or DEFAULT_FAST_MODEL, "balanced": balanced, "expert": config.get("expert_model") or DEFAULT_EXPERT_MODEL}


def choose_route(query: str, requested_mode: str, models: dict[str, str]) -> dict[str, Any]:
    assessment = assess_complexity(query)
    selected_mode = requested_mode
    if requested_mode == "auto":
        selected_mode = "quick" if assessment["complexity"] == "simple" else "balanced" if assessment["complexity"] == "standard" else "deep"
    if selected_mode == "quick":
        stages = [{"name": "answer", "purpose": "single-pass fast lookup", "model": models["fast"]}]
    elif selected_mode == "balanced":
        stages = [{"name": "answer", "purpose": "single-pass balanced search", "model": models["balanced"]}]
    elif selected_mode == "expert":
        stages = [{"name": "answer", "purpose": "single-pass expert synthesis", "model": models["expert"]}]
    elif selected_mode == "deep":
        stages = [
            {"name": "scout", "purpose": "fast scouting + task decomposition", "model": models["fast"]},
            {"name": "gap_fill", "purpose": "targeted fast gap closing if needed", "model": models["fast"], "optional": True},
            {"name": "final", "purpose": "expert final synthesis", "model": models["expert"]},
        ]
    else:
        raise RuntimeError(f"Unsupported mode: {selected_mode}")
    return {"requested_mode": requested_mode, "selected_mode": selected_mode, **assessment, "stages": stages}


def stage_sources(text: str, raw: list[dict[str, Any]], max_sources: int) -> list[str]:
    urls = extract_urls(text)
    for item in raw:
        urls.extend(extract_payload_urls(item))
    return dedupe_keep_order(urls)[:max_sources]


def run_single_stage(query: str, model: str, base_url: str, api_key: str, max_sources: int, language: str, system_prompt: str = SYSTEM_PROMPT, required_sources: list[str] | None = None, stream: bool = False, timeout: int = 240, extra_body: dict[str, Any] | None = None) -> dict[str, Any]:
    started = time.time()
    reasoning, text, raw = post_chat_completion(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": build_single_user_prompt(query, max_sources, language, required_sources)}],
        model=model, base_url=base_url, api_key=api_key, stream=stream, timeout=timeout, extra_body=extra_body,
    )
    return {"model": model, "purpose": "single-pass answer", "text": text.strip(), "reasoning": reasoning, "sources": stage_sources(text, raw, max_sources), "raw": raw, "latency_seconds": round(time.time() - started, 2)}


def run_deep_route(query: str, models: dict[str, str], base_url: str, api_key: str, max_sources: int, language: str, required_sources: list[str] | None = None, stream: bool = False, timeout: int = 360, extra_body: dict[str, Any] | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    stages: list[dict[str, Any]] = []
    scout_started = time.time()
    scout_reasoning, scout_text, scout_raw = post_chat_completion(
        messages=[{"role": "system", "content": SCOUT_SYSTEM_PROMPT}, {"role": "user", "content": build_scout_prompt(query, max_sources, language, required_sources)}],
        model=models["fast"], base_url=base_url, api_key=api_key, temperature=0.1, stream=stream, timeout=timeout, extra_body=extra_body,
    )
    scout_stage = {"name": "scout", "model": models["fast"], "purpose": "fast scouting + task decomposition", "text": scout_text.strip(), "reasoning": scout_reasoning, "sources": stage_sources(scout_text, scout_raw, max_sources), "latency_seconds": round(time.time() - scout_started, 2)}
    stages.append(scout_stage)

    gap_notes = ""
    gaps = extract_gap_candidates(scout_text)
    if gaps:
        gap_started = time.time()
        gap_reasoning, gap_text, gap_raw = post_chat_completion(
            messages=[{"role": "system", "content": SCOUT_SYSTEM_PROMPT}, {"role": "user", "content": build_gap_fill_prompt(query, scout_text, gaps, max_sources, language, required_sources)}],
            model=models["fast"], base_url=base_url, api_key=api_key, temperature=0.1, stream=stream, timeout=timeout, extra_body=extra_body,
        )
        gap_notes = gap_text.strip()
        stages.append({"name": "gap_fill", "model": models["fast"], "purpose": "targeted fast gap closing", "text": gap_notes, "reasoning": gap_reasoning, "sources": stage_sources(gap_text, gap_raw, max_sources), "latency_seconds": round(time.time() - gap_started, 2)})

    final_started = time.time()
    final_reasoning, final_text, final_raw = post_chat_completion(
        messages=[{"role": "system", "content": EXPERT_SYSTEM_PROMPT}, {"role": "user", "content": build_expert_prompt(query, scout_text, gap_notes or None, max_sources, language, required_sources)}],
        model=models["expert"], base_url=base_url, api_key=api_key, temperature=0.15, stream=stream, timeout=timeout, extra_body=extra_body,
    )
    final_stage = {"name": "final", "model": models["expert"], "purpose": "expert final synthesis", "text": final_text.strip(), "reasoning": final_reasoning, "sources": stage_sources(final_text, final_raw, max_sources), "latency_seconds": round(time.time() - final_started, 2), "raw": final_raw}
    stages.append(final_stage)
    return final_stage, stages


def build_result(query: str, route: dict[str, Any], base_url: str, final_stage: dict[str, Any], stages: list[dict[str, Any]], max_sources: int) -> dict[str, Any]:
    all_sources: list[str] = []
    for stage in [final_stage] + stages:
        all_sources.extend(stage.get("sources", []))
    safe_stages = [{"name": s.get("name"), "model": s.get("model"), "purpose": s.get("purpose"), "text": truncate_text(s.get("text", ""), 4000), "sources": s.get("sources", []), "latency_seconds": s.get("latency_seconds")} for s in stages]
    return {"query": query, "model": final_stage.get("model"), "route": route, "base_url": base_url, "overview": final_stage.get("text", "").strip(), "search_results": final_stage.get("text", "").strip(), "sources": dedupe_keep_order(all_sources)[:max_sources], "reasoning": final_stage.get("reasoning", ""), "stages": safe_stages, "raw_response": final_stage.get("raw", [])}


def print_text_output(result: dict[str, Any], show_reasoning: bool = False, show_plan: bool = False) -> None:
    route = result.get("route") or {}
    if show_plan:
        print("策略：")
        print(f"- requested_mode: {route.get('requested_mode')}")
        print(f"- selected_mode: {route.get('selected_mode')}")
        if route.get("complexity"):
            print(f"- complexity: {route.get('complexity')} (score={route.get('complexity_score')})")
        stages = route.get("stages") or []
        if stages:
            print("- stages: " + " -> ".join(str(stage.get("model")) for stage in stages if stage.get("model")))
        if route.get("source_requirements"):
            print("- source_requirements: " + ", ".join(route["source_requirements"]))
        print()
    if show_reasoning and result.get("reasoning"):
        print("Reasoning:\n" + result["reasoning"] + "\n")
    print(f"概述：{result.get('overview', '').strip()}")
    print("搜索结果：")
    print(result.get("search_results", "").strip())
    print("来源：")
    for i, url in enumerate(result.get("sources", []), 1):
        print(f"{i}. {url}")


def main() -> int:
    config = load_config()
    models = resolve_models(config)
    parser = argparse.ArgumentParser(description="Adaptive Perplexity search/deep-research via HTTP chat completions")
    parser.add_argument("--query", required=True, help="Search query / latest-information request")
    parser.add_argument("--mode", choices=["auto", "quick", "balanced", "expert", "deep"], default=config.get("default_mode", DEFAULT_MODE), help="Routing mode")
    parser.add_argument("--model", default=None, help="Force a specific model and skip automatic routing")
    parser.add_argument("--base-url", default=config.get("base_url", DEFAULT_BASE_URL), help="Perplexity/OpenAI-compatible base URL override")
    parser.add_argument("--api-key", default=config.get("api_key", ""), help="API key override")
    parser.add_argument("--max-sources", type=int, default=int(config.get("max_sources", 5)), help="Maximum number of source URLs to keep")
    parser.add_argument("--language", default=config.get("language", "zh-CN"), help="Preferred reply language")
    parser.add_argument("--timeout", type=int, default=int(config.get("timeout_seconds", 240)), help="HTTP timeout seconds")
    parser.add_argument("--stream", action="store_true", default=bool(config.get("stream", False)), help="Use SSE streaming if the endpoint supports it")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--show-reasoning", action="store_true", help="Print reasoning before final answer")
    parser.add_argument("--show-plan", action="store_true", help="Print routing / plan metadata before final answer")
    args = parser.parse_args()

    max_sources = max(1, args.max_sources)
    required_sources = get_technical_required_sources(config) if is_technical_query(args.query) else []
    extra_body = config.get("extra_body") if isinstance(config.get("extra_body"), dict) else None

    if args.model:
        route = {"requested_mode": args.mode, "selected_mode": "forced-model", "complexity": None, "complexity_score": None, "reasons": ["explicit --model override"], "source_requirements": required_sources, "stages": [{"name": "answer", "purpose": "single-pass forced model", "model": args.model}]}
        single = run_single_stage(args.query, args.model, args.base_url, args.api_key, max_sources, args.language, required_sources=required_sources, stream=args.stream, timeout=args.timeout, extra_body=extra_body)
        single["purpose"] = "single-pass forced model"
        final_stage = single | {"name": "final"}
        result = build_result(args.query, route, args.base_url, final_stage, [final_stage], max_sources)
    else:
        route = choose_route(args.query, args.mode, models)
        route["source_requirements"] = required_sources
        selected_mode = route["selected_mode"]
        if selected_mode == "deep":
            final_stage, stages = run_deep_route(args.query, models, args.base_url, args.api_key, max_sources, args.language, required_sources=required_sources, stream=args.stream, timeout=args.timeout, extra_body=extra_body)
            result = build_result(args.query, route, args.base_url, final_stage, stages, max_sources)
        else:
            key = "fast" if selected_mode == "quick" else "expert" if selected_mode == "expert" else "balanced"
            single = run_single_stage(args.query, models[key], args.base_url, args.api_key, max_sources, args.language, required_sources=required_sources, stream=args.stream, timeout=args.timeout, extra_body=extra_body)
            single["purpose"] = route["stages"][0]["purpose"]
            final_stage = single | {"name": "final"}
            result = build_result(args.query, route, args.base_url, final_stage, [final_stage], max_sources)

    if args.json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_text_output(result, show_reasoning=args.show_reasoning, show_plan=args.show_plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
