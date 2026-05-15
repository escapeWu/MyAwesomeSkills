#!/usr/bin/env python3
"""Adaptive AI-enhanced web/news search via chat completions + SSE parsing."""

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
DEFAULT_MODEL = "grok-4.20-auto"
DEFAULT_BASE_URL = "https://example.com/v1/"
DEFAULT_FAST_MODEL = "grok-4.20-fast"
DEFAULT_EXPERT_MODEL = "grok-4.20-expert"
DEFAULT_MODE = "auto"
MAX_STAGE_NOTE_CHARS = 6000

SYSTEM_PROMPT = (
    "You are a fast web-aware research assistant. "
    "Focus on the latest relevant information. "
    "Answer concisely, and always include source URLs in a final Sources section. "
    "If recency matters, prioritize the newest reliable information."
)

SCOUT_SYSTEM_PROMPT = (
    "You are a stage-1 web scout. Work quickly. "
    "Identify the newest hard facts, the most important sub-questions, and the remaining gaps. "
    "Always include source URLs."
)

EXPERT_SYSTEM_PROMPT = (
    "You are a stage-2 expert web research synthesizer. "
    "Use the scout notes as hints, but independently re-check important claims with fresh web-aware retrieval. "
    "Return a structured, high-signal final answer with source URLs."
)

COMPLEX_KEYWORDS = [
    "compare",
    "comparison",
    "vs",
    "versus",
    "tradeoff",
    "analyze",
    "analysis",
    "investigate",
    "investigation",
    "audit",
    "deep",
    "research",
    "timeline",
    "cross-check",
    "verify",
    "contradiction",
    "root cause",
    "synthesize",
    "评估",
    "分析",
    "比较",
    "对比",
    "调研",
    "调查",
    "深度",
    "审计",
    "时间线",
    "影响",
    "原因",
    "矛盾",
    "交叉验证",
    "拆解",
]

SIMPLE_HINTS = [
    "latest",
    "today",
    "current",
    "news",
    "price",
    "weather",
    "what is",
    "谁是",
    "是什么",
    "最新",
    "刚刚",
    "价格",
    "行情",
]


def load_config() -> dict[str, str]:
    if not CONFIG_PATH.exists():
        raise RuntimeError(f"Missing config file: {CONFIG_PATH}")
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid config.json format: {CONFIG_PATH}")
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
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n[truncated]"


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
                text = item.get("text") or item.get("content") or ""
                if text:
                    parts.append(str(text))
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

                try:
                    chunk, end = decoder.raw_decode(data_str)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"Failed to parse SSE JSON chunk: {data_str[:200]!r}") from exc

                remainder = data_str[end:].strip()
                if remainder:
                    raise RuntimeError(f"Unexpected extra data after SSE JSON: {remainder[:200]!r}")
                if not isinstance(chunk, dict):
                    continue

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


def post_chat_completion(messages: list[dict[str, str]], model: str, base_url: str, api_key: str, temperature: float = 0.2) -> tuple[str, str, list[dict[str, Any]]]:
    if not api_key:
        raise RuntimeError(f"Missing api_key in {CONFIG_PATH}")

    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream, application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": True,
    }

    with requests.post(url, headers=headers, json=payload, timeout=180, stream=True) as response:
        response.raise_for_status()
        content_type = (response.headers.get("content-type") or "").lower()
        if "text/event-stream" in content_type:
            return parse_sse_response(response)
        if "application/json" in content_type:
            return parse_json_response(response)
        raise RuntimeError(f"Unsupported response content-type={content_type!r}")


def build_single_user_prompt(query: str, max_sources: int, language: str) -> str:
    return (
        f"User query: {query}\n\n"
        "Find the latest relevant information from the web. "
        "Return a concise answer first, then a 'Sources:' section with numbered source URLs. "
        f"Limit the sources section to at most {max_sources} URLs. "
        f"Reply in {language}."
    )


def build_scout_prompt(query: str, max_sources: int, language: str) -> str:
    return (
        f"Original task: {query}\n\n"
        "Do a fast scouting pass. "
        "Break the task into the minimum useful sub-questions, collect the newest hard facts, "
        "and explicitly note what still needs verification.\n\n"
        "Return exactly these sections:\n"
        "Summary:\n"
        "Claims to verify:\n"
        "Key gaps:\n"
        "Sources:\n"
        f"Keep it compact. Limit Sources to at most {max_sources} URLs. Reply in {language}."
    )


def build_gap_fill_prompt(query: str, scout_notes: str, gaps: list[str], max_sources: int, language: str) -> str:
    gap_text = "\n".join(f"- {gap}" for gap in gaps[:6]) or "- No explicit gaps extracted; focus on weakly supported claims."
    return (
        f"Original task: {query}\n\n"
        "Stage-1 scout notes:\n"
        f"{truncate_text(scout_notes, 3000)}\n\n"
        "Focus ONLY on the unresolved gaps below and return targeted facts that close them:\n"
        f"{gap_text}\n\n"
        "Return exactly these sections:\n"
        "Gap findings:\n"
        "What is now resolved:\n"
        "Remaining uncertainty:\n"
        "Sources:\n"
        f"Limit Sources to at most {max_sources} URLs. Reply in {language}."
    )


def build_expert_prompt(query: str, scout_notes: str, gap_notes: str | None, max_sources: int, language: str) -> str:
    sections = [
        f"Original task: {query}",
        "",
        "Stage-1 scout notes:",
        truncate_text(scout_notes),
    ]
    if gap_notes:
        sections.extend(["", "Gap-fill notes:", truncate_text(gap_notes)])
    sections.extend(
        [
            "",
            "Now produce the final answer.",
            "Re-check important claims with fresh web-aware retrieval rather than blindly trusting the notes above.",
            "Return a concise but complete answer first, then a 'Sources:' section with numbered URLs.",
            f"Limit Sources to at most {max_sources} URLs.",
            f"Reply in {language}.",
        ]
    )
    return "\n".join(sections)


def extract_gap_candidates(text: str) -> list[str]:
    match = re.search(
        r"(?:Key gaps|Gaps|Missing information|Remaining uncertainty)\s*:\s*(.*?)(?:\n(?:Sources|Gap findings|What is now resolved|Summary|Claims to verify)\s*:|\Z)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return []
    body = match.group(1).strip()
    items: list[str] = []
    for line in body.splitlines():
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
        score += 2
        reasons.append("query is fairly long")
    if len(q) > 280:
        score += 1
        reasons.append("query is very long")

    keyword_hits = [kw for kw in COMPLEX_KEYWORDS if kw in lower or kw in q]
    if keyword_hits:
        score += min(4, len(keyword_hits))
        reasons.append("contains analytical / investigative language")

    if len(re.findall(r"[?？]", q)) >= 2:
        score += 1
        reasons.append("contains multiple explicit questions")

    separators = [",", "，", ";", "；", " and ", "以及", "同时", "并且"]
    separator_hits = sum(1 for sep in separators if sep in lower or sep in q)
    if separator_hits >= 2:
        score += 1
        reasons.append("asks for multiple dimensions or sub-parts")

    if any(token in lower or token in q for token in ["source", "sources", "with links", "引用", "来源", "证据"]):
        score += 1
        reasons.append("explicitly asks for sources / evidence")

    simple_hits = [kw for kw in SIMPLE_HINTS if kw in lower or kw in q]
    if simple_hits and len(q) < 90 and not keyword_hits:
        score -= 1
        reasons.append("looks like a short freshness-sensitive lookup")

    if score <= 1:
        label = "simple"
    elif score <= 4:
        label = "standard"
    else:
        label = "complex"

    return {
        "complexity": label,
        "complexity_score": max(score, 0),
        "reasons": reasons or ["default routing"],
        "keyword_hits": keyword_hits[:8],
    }


def resolve_models(config: dict[str, str]) -> dict[str, str]:
    balanced = config.get("auto_model") or config.get("model") or DEFAULT_MODEL
    return {
        "fast": config.get("fast_model") or DEFAULT_FAST_MODEL,
        "balanced": balanced,
        "expert": config.get("expert_model") or DEFAULT_EXPERT_MODEL,
    }


def choose_route(query: str, requested_mode: str, models: dict[str, str]) -> dict[str, Any]:
    assessment = assess_complexity(query)
    selected_mode = requested_mode
    if requested_mode == "auto":
        if assessment["complexity"] == "simple":
            selected_mode = "quick"
        elif assessment["complexity"] == "standard":
            selected_mode = "balanced"
        else:
            selected_mode = "deep"

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

    return {
        "requested_mode": requested_mode,
        "selected_mode": selected_mode,
        **assessment,
        "stages": stages,
    }


def run_single_stage(query: str, model: str, base_url: str, api_key: str, max_sources: int, language: str, system_prompt: str = SYSTEM_PROMPT) -> dict[str, Any]:
    started = time.time()
    reasoning, text, raw = post_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": build_single_user_prompt(query, max_sources, language)},
        ],
        model=model,
        base_url=base_url,
        api_key=api_key,
    )
    return {
        "model": model,
        "purpose": "single-pass answer",
        "text": text.strip(),
        "reasoning": reasoning,
        "sources": extract_urls(text)[:max_sources],
        "raw": raw,
        "latency_seconds": round(time.time() - started, 2),
    }


def run_deep_route(query: str, models: dict[str, str], base_url: str, api_key: str, max_sources: int, language: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    stages: list[dict[str, Any]] = []

    scout_started = time.time()
    scout_reasoning, scout_text, scout_raw = post_chat_completion(
        messages=[
            {"role": "system", "content": SCOUT_SYSTEM_PROMPT},
            {"role": "user", "content": build_scout_prompt(query, max_sources, language)},
        ],
        model=models["fast"],
        base_url=base_url,
        api_key=api_key,
        temperature=0.1,
    )
    scout_stage = {
        "name": "scout",
        "model": models["fast"],
        "purpose": "fast scouting + task decomposition",
        "text": scout_text.strip(),
        "reasoning": scout_reasoning,
        "sources": extract_urls(scout_text)[:max_sources],
        "latency_seconds": round(time.time() - scout_started, 2),
    }
    stages.append(scout_stage)

    gap_notes = ""
    gaps = extract_gap_candidates(scout_text)
    if gaps:
        gap_started = time.time()
        gap_reasoning, gap_text, _gap_raw = post_chat_completion(
            messages=[
                {"role": "system", "content": SCOUT_SYSTEM_PROMPT},
                {"role": "user", "content": build_gap_fill_prompt(query, scout_text, gaps, max_sources, language)},
            ],
            model=models["fast"],
            base_url=base_url,
            api_key=api_key,
            temperature=0.1,
        )
        gap_notes = gap_text.strip()
        stages.append(
            {
                "name": "gap_fill",
                "model": models["fast"],
                "purpose": "targeted fast gap closing",
                "text": gap_notes,
                "reasoning": gap_reasoning,
                "sources": extract_urls(gap_text)[:max_sources],
                "latency_seconds": round(time.time() - gap_started, 2),
            }
        )

    final_started = time.time()
    final_reasoning, final_text, final_raw = post_chat_completion(
        messages=[
            {"role": "system", "content": EXPERT_SYSTEM_PROMPT},
            {"role": "user", "content": build_expert_prompt(query, scout_text, gap_notes or None, max_sources, language)},
        ],
        model=models["expert"],
        base_url=base_url,
        api_key=api_key,
        temperature=0.15,
    )
    final_stage = {
        "name": "final",
        "model": models["expert"],
        "purpose": "expert final synthesis",
        "text": final_text.strip(),
        "reasoning": final_reasoning,
        "sources": extract_urls(final_text)[:max_sources],
        "latency_seconds": round(time.time() - final_started, 2),
        "raw": final_raw,
    }
    stages.append(final_stage)
    return final_stage, stages


def build_result(query: str, route: dict[str, Any], base_url: str, final_stage: dict[str, Any], stages: list[dict[str, Any]], max_sources: int) -> dict[str, Any]:
    stage_sources: list[str] = []
    for stage in stages:
        stage_sources.extend(stage.get("sources", []))
    sources = dedupe_keep_order((final_stage.get("sources") or []) + stage_sources)[:max_sources]
    safe_stages = []
    for stage in stages:
        safe_stages.append(
            {
                "name": stage.get("name"),
                "model": stage.get("model"),
                "purpose": stage.get("purpose"),
                "text": truncate_text(stage.get("text", ""), 4000),
                "sources": stage.get("sources", []),
                "latency_seconds": stage.get("latency_seconds"),
            }
        )
    return {
        "query": query,
        "model": final_stage.get("model"),
        "route": route,
        "base_url": base_url,
        "overview": final_stage.get("text", "").strip(),
        "search_results": final_stage.get("text", "").strip(),
        "sources": sources,
        "reasoning": final_stage.get("reasoning", ""),
        "stages": safe_stages,
        "raw_response": final_stage.get("raw", []),
    }


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
        reasons = route.get("reasons") or []
        if reasons:
            print("- reasons: " + "; ".join(reasons))
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

    parser = argparse.ArgumentParser(description="Adaptive AI-enhanced fresh web search via Grok chat completions")
    parser.add_argument("--query", required=True, help="Search query / latest-news request")
    parser.add_argument("--mode", choices=["auto", "quick", "balanced", "expert", "deep"], default=config.get("default_mode", DEFAULT_MODE), help="Routing mode")
    parser.add_argument("--model", default=None, help="Force a specific model and skip automatic routing")
    parser.add_argument("--base-url", default=config.get("base_url", DEFAULT_BASE_URL), help="OpenAI-compatible base URL override")
    parser.add_argument("--api-key", default=config.get("api_key", ""), help="API key override")
    parser.add_argument("--max-sources", type=int, default=5, help="Maximum number of source URLs to keep")
    parser.add_argument("--language", default=config.get("language", "zh-CN"), help="Preferred reply language")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--show-reasoning", action="store_true", help="Print reasoning before final answer")
    parser.add_argument("--show-plan", action="store_true", help="Print routing / plan metadata before final answer")
    args = parser.parse_args()

    max_sources = max(1, args.max_sources)

    if args.model:
        route = {
            "requested_mode": args.mode,
            "selected_mode": "forced-model",
            "complexity": None,
            "complexity_score": None,
            "reasons": ["explicit --model override"],
            "stages": [{"name": "answer", "purpose": "single-pass forced model", "model": args.model}],
        }
        single = run_single_stage(args.query, args.model, args.base_url, args.api_key, max_sources, args.language)
        single["purpose"] = "single-pass forced model"
        final_stage = single | {"name": "final"}
        result = build_result(args.query, route, args.base_url, final_stage, [final_stage], max_sources)
    else:
        route = choose_route(args.query, args.mode, models)
        selected_mode = route["selected_mode"]
        if selected_mode == "deep":
            final_stage, stages = run_deep_route(args.query, models, args.base_url, args.api_key, max_sources, args.language)
            result = build_result(args.query, route, args.base_url, final_stage, stages, max_sources)
        else:
            key = "balanced"
            if selected_mode == "quick":
                key = "fast"
            elif selected_mode == "expert":
                key = "expert"
            single = run_single_stage(args.query, models[key], args.base_url, args.api_key, max_sources, args.language)
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
