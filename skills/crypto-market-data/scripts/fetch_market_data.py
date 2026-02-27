#!/usr/bin/env python3
"""
Fetch crypto market data in parallel:
  - Funding rate
  - Long/short ratio
  - Fear & greed index
  - K-line screenshots for 15m / 1h / 4h / 1d

Usage:
  python fetch_market_data.py [COINPAIR] [--base-url URL] [--api-key KEY]

  COINPAIR  defaults to BTC/USDT
  --base-url defaults to http://localhost:5174
  --api-key  Bearer token (can also be set via AITRADE_API_KEY env var)

Examples:
  python fetch_market_data.py
  python fetch_market_data.py ETH/USDT
  python fetch_market_data.py BTC/USDT --base-url https://agent-toolkit.01010101.xyz --api-key <token>
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip install requests")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------

def _get(session: "requests.Session", url: str, label: str) -> dict:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return {"label": label, "data": r.json()}


def _post(session: "requests.Session", url: str, body: dict, label: str) -> dict:
    r = session.post(url, json=body, timeout=60)
    r.raise_for_status()
    return {"label": label, "data": r.json()}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def fetch_all(coinpair: str, base_url: str, api_key: str) -> dict:
    """Fire all requests in parallel and return a dict keyed by label."""
    # Binance symbol: strip "/" and uppercase
    symbol = coinpair.replace("/", "").upper()

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    session = requests.Session()
    session.headers.update(headers)

    # Screenshot capture bodies (standard 4-period config)
    screenshot_tasks = [
        {
            "label": "screenshot_15m",
            "body": {"pair": coinpair, "kline_interval": "15m", "vol": True},
        },
        {
            "label": "screenshot_1h",
            "body": {"pair": coinpair, "kline_interval": "1h", "rsi": "6_12_24", "smc": True},
        },
        {
            "label": "screenshot_4h",
            "body": {"pair": coinpair, "kline_interval": "4h", "macd": "14_28_10", "vol": True},
        },
        {
            "label": "screenshot_1d",
            "body": {"pair": coinpair, "kline_interval": "1d", "ema": "20_50_200", "vol": True},
        },
    ]

    capture_url = f"{base_url}/api/analysis/screenshot-tasks/capture"
    sentiment_url = f"{base_url}/api/market/sentiment?symbol={symbol}"

    futures = {}
    results = {}

    with ThreadPoolExecutor(max_workers=6) as pool:
        # Market sentiment (single aggregated endpoint)
        futures[pool.submit(_get, session, sentiment_url, "sentiment")] = "sentiment"

        # Screenshots
        for task in screenshot_tasks:
            f = pool.submit(_post, session, capture_url, task["body"], task["label"])
            futures[f] = task["label"]

        for future in as_completed(futures):
            label = futures[future]
            try:
                result = future.result()
                results[result["label"]] = result["data"]
            except Exception as exc:
                results[label] = {"error": str(exc)}

    return results


def print_results(coinpair: str, results: dict) -> None:
    print(f"\n{'='*60}")
    print(f"  Market Data: {coinpair}")
    print(f"{'='*60}\n")

    # --- Sentiment ---
    s = results.get("sentiment", {})
    if "error" in s:
        print(f"[sentiment] ERROR: {s['error']}")
    else:
        fr = s.get("funding_rate", {})
        ls = s.get("long_short_ratio", {})
        fg = s.get("fear_greed", {}).get("data", [{}])[0]
        ga = (ls.get("global_account") or [{}])[0]

        print("### Funding Rate")
        print(f"  Mark Price   : {fr.get('mark_price')} USDT")
        print(f"  Funding Rate : {fr.get('funding_rate_pct')} "
              f"({'short pays long' if (fr.get('funding_rate') or 0) < 0 else 'long pays short'})")
        print()

        print("### Long/Short Ratio (1H global accounts)")
        print(f"  Long  : {ga.get('long_account', 'N/A'):.2%}" if isinstance(ga.get('long_account'), float) else f"  Long  : {ga.get('long_account', 'N/A')}")
        print(f"  Short : {ga.get('short_account', 'N/A'):.2%}" if isinstance(ga.get('short_account'), float) else f"  Short : {ga.get('short_account', 'N/A')}")
        print(f"  Ratio : {ga.get('long_short_ratio', 'N/A')}")
        print()

        print("### Fear & Greed Index")
        print(f"  Value : {fg.get('value')} ({fg.get('label')})")
        print()

    # --- Screenshots ---
    print("### K-Line Screenshots")
    for tf in ["15m", "1h", "4h", "1d"]:
        key = f"screenshot_{tf}"
        d = results.get(key, {})
        if "error" in d:
            print(f"  [{tf:>3}] ERROR: {d['error']}")
        else:
            url = d.get("url", "N/A")
            print(f"  [{tf:>3}] {url}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Fetch crypto market data in parallel")
    parser.add_argument("coinpair", nargs="?", default="BTC/USDT",
                        help="Trading pair, e.g. ETH/USDT (default: BTC/USDT)")
    parser.add_argument("--base-url", default=os.getenv("AITRADE_BASE_URL", "http://localhost:5174"),
                        help="AI Trade Toolkit base URL")
    parser.add_argument("--api-key", default=os.getenv("AITRADE_API_KEY", ""),
                        help="Bearer token for API authentication")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    args = parser.parse_args()

    results = fetch_all(args.coinpair, args.base_url.rstrip("/"), args.api_key)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_results(args.coinpair, results)


if __name__ == "__main__":
    main()
