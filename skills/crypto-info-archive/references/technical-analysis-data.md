# Technical Analysis Data (技术分析数据)

## Overview

Technical analysis records store structured analysis reports for crypto trading pairs. Each record contains analysis conclusions, tagged by symbol and analysis type.

## Data Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | Yes | Trading pair, e.g. `BTC/USDT`, `ETH/USDT` |
| title | string | Yes | Analysis title summarizing the conclusion |
| content | string | Yes | Full analysis text (supports markdown) |
| tags | string[] | No | Classification tags, e.g. `["daily", "trend", "support-resistance"]` |
| create_time | datetime (ISO 8601) | Yes | When the analysis was produced |

## Deduplication

Records are deduplicated by `(symbol, title, create_time)`. Duplicate inserts are silently ignored.

## Authentication

The analysis write endpoint requires an API key with `analysis` permission. Pass the key via the `X-API-Key` header.

## API Endpoints

### Create Record
```
POST /api/analysis
X-API-Key: <your-api-key>
Content-Type: application/json

{
  "symbol": "BTC/USDT",
  "title": "BTC daily trend analysis",
  "content": "BTC is testing the 65000 resistance level...",
  "tags": ["daily", "trend"],
  "create_time": "2026-02-21T08:00:00Z"
}
```

### Query Records
```
GET /api/analysis?symbol=BTC/USDT&tag=daily&start_time=2026-02-01T00:00:00Z&limit=50&offset=0
```
Supports filtering by `symbol`, `tag`, `start_time`, `end_time`, with pagination.

### Attachments
```
POST /api/analysis/{record_id}/attachments  (multipart file upload, e.g. chart images)
DELETE /api/analysis/{record_id}/attachments/{attachment_id}
```

## Writing Guidelines

1. Use consistent `symbol` format: `BASE/QUOTE` (e.g. `BTC/USDT`, not `BTCUSDT`).
2. Use descriptive `tags` for filtering:
   - Timeframe: `1h`, `4h`, `daily`, `weekly`
   - Type: `trend`, `support-resistance`, `pattern`, `indicator`
   - Signal: `bullish`, `bearish`, `consolidation`
3. Set `create_time` to when the analysis was performed.
4. Structure `content` in markdown for readability. Include key levels, indicators, and conclusions.
5. Attach chart images via the attachments endpoint after creating the record.
