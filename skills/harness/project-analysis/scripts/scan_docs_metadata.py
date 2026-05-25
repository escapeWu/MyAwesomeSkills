#!/usr/bin/env python3
"""
scan_docs_metadata.py - 扫描 docs 目录下的分析文档，提取 YAML frontmatter metadata。

用法：
    python3 scan_docs_metadata.py [docs_dir]

参数：
    docs_dir  可选，docs 目录路径，默认为当前目录下的 docs/

输出：
    JSON 格式的文档 metadata 列表，包含文件路径、metadata 字段和内容摘要。
"""

import os
import sys
import json
import re
from pathlib import Path


def extract_frontmatter(filepath: str) -> dict | None:
    """从 markdown 文件中提取 YAML frontmatter。"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None

    # 匹配 --- 开头和结尾的 YAML frontmatter
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None

    yaml_text = match.group(1)
    metadata = {}

    # 简易 YAML 解析（避免依赖 PyYAML）
    current_key = None
    list_buffer = []

    for line in yaml_text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue

        # 列表项
        if line_stripped.startswith("- "):
            value = line_stripped[2:].strip().strip('"').strip("'")
            list_buffer.append(value)
            if current_key:
                metadata[current_key] = list_buffer
            continue

        # key: value 对
        if ":" in line_stripped:
            # 保存之前的列表
            colon_idx = line_stripped.index(":")
            key = line_stripped[:colon_idx].strip()
            value = line_stripped[colon_idx + 1 :].strip().strip('"').strip("'")

            current_key = key
            list_buffer = []

            if value:
                metadata[key] = value
            # value 为空表示后面可能是列表，先不赋值

    return metadata


def extract_summary(filepath: str, max_lines: int = 5) -> str:
    """提取文档内容摘要（跳过 frontmatter，取前几行正文或第一个标题）。"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return ""

    # 跳过 frontmatter
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, count=1, flags=re.DOTALL)
    lines = [l.strip() for l in body.strip().split("\n") if l.strip()]

    summary_lines = []
    for line in lines[:max_lines]:
        # 清理 markdown 标记
        clean = re.sub(r"^#+\s*", "", line)
        clean = re.sub(r"^>\s*", "", clean)
        if clean:
            summary_lines.append(clean)

    return " | ".join(summary_lines)


def scan_docs(docs_dir: str) -> list[dict]:
    """扫描 docs 目录，收集所有 .md 文件的 metadata。"""
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        return []

    results = []
    for md_file in sorted(docs_path.glob("**/*.md")):
        metadata = extract_frontmatter(str(md_file))
        if metadata is None:
            # 没有 frontmatter 的文件也记录，但标记为 unstructured
            metadata = {"_unstructured": True}

        result = {
            "file": str(md_file.relative_to(docs_path)),
            "path": str(md_file),
            "metadata": metadata,
            "summary": extract_summary(str(md_file)),
        }
        results.append(result)

    return results


def main():
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"

    if not os.path.isdir(docs_dir):
        print(json.dumps({"docs_dir": docs_dir, "exists": False, "documents": []}))
        sys.exit(0)

    documents = scan_docs(docs_dir)

    output = {
        "docs_dir": docs_dir,
        "exists": True,
        "count": len(documents),
        "documents": documents,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
