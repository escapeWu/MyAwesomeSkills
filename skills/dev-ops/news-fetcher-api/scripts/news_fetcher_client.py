#!/usr/bin/env python3
"""Small dependency-free client for the news fetcher REST API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

DEFAULT_BASE_URL = "https://<news-fetcher-host>"


def env_base() -> str:
    return os.environ.get("NEWS_FETCHER_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def env_token(required: bool) -> str | None:
    token = os.environ.get("NEWS_FETCHER_TOKEN")
    if required and not token:
        raise SystemExit("NEWS_FETCHER_TOKEN is required for this command")
    return token


def request(method: str, path: str, *, token: str | None = None, query: dict[str, Any] | None = None, body: dict[str, Any] | None = None) -> tuple[int, Any]:
    base = env_base()
    url = base + path
    if query:
        clean = {k: v for k, v in query.items() if v is not None}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)
    data = None
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.status, parse_body(raw)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        return exc.code, parse_body(raw)


def parse_body(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def dump(status: int, payload: Any) -> None:
    print(f"HTTP {status}")
    print(json.dumps(payload, ensure_ascii=False, indent=2) if not isinstance(payload, str) else payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="News fetcher REST API helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("sites")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("discover")
    p.add_argument("domain")
    p.add_argument("--since", default="7d")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--site")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("fetch")
    p.add_argument("url")

    p = sub.add_parser("history")
    p.add_argument("--domain")
    p.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()

    if args.cmd == "sites":
        status, payload = request("GET", "/v1/sites", token=env_token(True), query={"limit": args.limit})
    elif args.cmd == "discover":
        status, payload = request("GET", f"/v1/discover/{urllib.parse.quote(args.domain)}", token=env_token(True), query={"since": args.since, "limit": args.limit})
    elif args.cmd == "search":
        status, payload = request("GET", "/v1/search", token=env_token(True), query={"query": args.query, "site": args.site, "limit": args.limit})
    elif args.cmd == "fetch":
        status, payload = request("POST", "/v1/fetch", token=env_token(True), body={"url": args.url})
    elif args.cmd == "history":
        status, payload = request("GET", "/v1/history", token=env_token(True), query={"domain": args.domain, "limit": args.limit})
    else:  # pragma: no cover
        parser.error(f"unknown command: {args.cmd}")

    dump(status, payload)
    return 0 if status < 400 else 1


if __name__ == "__main__":
    sys.exit(main())
