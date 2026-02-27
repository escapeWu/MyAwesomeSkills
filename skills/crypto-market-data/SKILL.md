---
name: crypto-market-data
description: Fetch funding rate, long/short ratio, fear & greed index, and K-line screenshots (15m/1h/4h/1d) for any trading pair in one parallel batch via the AI Trade Toolkit API. Default pair BTC/USDT.
---

# crypto-market-data

Fetch all market data for a trading pair in a single parallel run using
`scripts/fetch_market_data.py`. All 5 HTTP requests fire concurrently via `ThreadPoolExecutor`.

## Quick Start

```bash
# BTC/USDT (default)
python3 scripts/fetch_market_data.py \
  --base-url <BASE_URL> \
  --api-key   <API_KEY>

# Specific pair
python3 scripts/fetch_market_data.py ETH/USDT \
  --base-url <BASE_URL> \
  --api-key   <API_KEY>

# Output raw JSON (useful for piping into other tools)
python3 scripts/fetch_market_data.py BTC/USDT --json \
  --base-url <BASE_URL> \
  --api-key   <API_KEY>
```

Set env vars to avoid repeating flags:
```bash
export AITRADE_BASE_URL=https://agent-toolkit.01010101.xyz
export AITRADE_API_KEY=<token>
python3 scripts/fetch_market_data.py ETH/USDT
```

Dependency: `pip install requests`

## What the Script Fetches (all in parallel)

| # | Data | Endpoint |
|---|---|---|
| 1 | Funding rate + mark price | `GET /api/market/sentiment?symbol=<SYMBOL>` |
| 2 | Long/short ratio (1H) | same aggregated response |
| 3 | Fear & greed index | same aggregated response |
| 4 | 15m K-line screenshot | `POST /api/analysis/screenshot-tasks/capture` |
| 5 | 1H K-line (RSI + SMC) | same endpoint |
| 6 | 4H K-line (MACD + vol) | same endpoint |
| 7 | 1D K-line (EMA + vol) | same endpoint |

## Screenshot Indicator Configuration

| Timeframe | Indicators | Purpose |
|---|---|---|
| 15m | vol | Entry precision, volume confirmation |
| 1H | RSI(6/12/24) + SMC | Short-term overbought/oversold + market structure |
| 4H | MACD(14/28/10) + vol | Mid-term momentum divergence |
| 1D | EMA(20/50/200) + vol | Trend direction |

## Output

**Formatted (default):**
```
=== Market Data: ETH/USDT ===

### Funding Rate
  Mark Price   : 1953.33 USDT
  Funding Rate : -0.0111% (short pays long)

### Long/Short Ratio (1H global accounts)
  Long  : 67.88%
  Short : 32.12%
  Ratio : 2.1133

### Fear & Greed Index
  Value : 13 (Extreme Fear)

### K-Line Screenshots
  [15m] https://rustfs.../kline_ETH_USDT_15m_....png
  [ 1h] https://rustfs.../kline_ETH_USDT_1h_....png
  [ 4h] https://rustfs.../kline_ETH_USDT_4h_....png
  [ 1d] https://rustfs.../kline_ETH_USDT_1d_....png
```

**JSON (`--json`):** Dict keyed by `sentiment`, `screenshot_15m`, `screenshot_1h`,
`screenshot_4h`, `screenshot_1d`.

## Notes

- The `symbol` for the sentiment endpoint strips `/` and uppercases (`ETH/USDT` → `ETHUSDT`).
- Screenshot `ai_result` is `null` by default — the script omits `with_ai` to keep latency low.
- Per-request errors are reported individually without blocking other results.
