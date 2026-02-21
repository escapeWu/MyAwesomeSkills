---
name: crypto-info-archive
description: Guide for archiving crypto market information into the aitrade support server. Use when writing news/public opinion data to sentiment storage, or writing technical analysis reports to analysis storage. Covers data schemas, API usage, field conventions, and best practices for both sentiment (舆情) and technical analysis data types.
---

# Crypto Info Archive

Archive crypto market information (news sentiment and technical analysis) into the aitrade support server's data store.

## Data Types

Two categories of data can be archived:

1. **Sentiment Data (舆情)** — News, public opinion, market sentiment records
2. **Technical Analysis Data** — Structured analysis reports for trading pairs

## Workflow

1. Determine the data type (sentiment or technical analysis)
2. Read the corresponding reference for schema and API details:
   - Sentiment: See [sentiment-data.md](references/sentiment-data.md)
   - Technical Analysis: See [technical-analysis-data.md](references/technical-analysis-data.md)
3. Format the data according to the schema
4. Call the appropriate API endpoint to write the data
5. Optionally attach files (charts, screenshots) to the created record

## Key Differences

| | Sentiment | Technical Analysis |
|---|---|---|
| Purpose | News & market opinion | Trading pair analysis |
| Identifier | `relation` (e.g. `BTC`) | `symbol` (e.g. `BTC/USDT`) |
| Classification | `opinion` field | `tags` array |
| Batch insert | Supported | Not supported |
| Auth required | No | Yes (`analysis` permission) |

## Configuration

The API base URL and API keys are environment-specific. Do not hardcode these values. Obtain them from the deployment configuration or environment variables.
