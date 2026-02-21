# Sentiment Data (舆情数据)

## Overview

Sentiment data stores news and public opinion records related to crypto assets. Each record represents a piece of news or market sentiment with an assessed opinion direction.

## Data Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | News headline or sentiment title |
| content | string | Yes | Full text content of the news/opinion |
| opinion | string | Yes | Sentiment direction: `positive`, `negative`, or `neutral` |
| create_time | datetime (ISO 8601) | Yes | When the news/event occurred |
| relation | string | Yes | Related trading pair symbol, e.g. `BTC`, `ETH`, `SOL` |

## Deduplication

Records are deduplicated by `(title, create_time)`. Duplicate inserts are silently ignored (ON CONFLICT DO NOTHING).

## API Endpoints

### Create Single Record
```
POST /api/sentiment
Content-Type: application/json

{
  "title": "Fed holds rates steady",
  "content": "The Federal Reserve kept interest rates unchanged...",
  "opinion": "neutral",
  "create_time": "2026-02-21T10:00:00Z",
  "relation": "BTC"
}
```

### Batch Create
```
POST /api/sentiment/batch
Content-Type: application/json

[
  {"title": "...", "content": "...", "opinion": "positive", "create_time": "...", "relation": "BTC"},
  {"title": "...", "content": "...", "opinion": "negative", "create_time": "...", "relation": "ETH"}
]
```
Response: `{"inserted": 2}` (count of actually inserted, excluding duplicates)

### Query Records
```
GET /api/sentiment?relation=BTC&start_time=2026-02-01T00:00:00Z&end_time=2026-02-21T23:59:59Z&limit=50&offset=0
```

### Attachments
```
POST /api/sentiment/{record_id}/attachments  (multipart file upload)
DELETE /api/sentiment/{record_id}/attachments/{attachment_id}
```

## Writing Guidelines

1. Set `opinion` based on the overall market impact assessment:
   - `positive` — bullish signal, favorable regulation, adoption news
   - `negative` — bearish signal, hack, regulatory crackdown
   - `neutral` — informational, mixed signals
2. Set `relation` to the most relevant symbol. Use broad symbols (e.g. `BTC`) for market-wide news.
3. Use `create_time` as the news publication time, not the time of archival.
4. Prefer batch insert when writing multiple records to reduce API calls.
5. Keep `title` concise (<200 chars). Put full analysis in `content`.
