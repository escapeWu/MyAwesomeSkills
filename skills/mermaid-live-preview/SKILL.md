---
name: mermaid-live-preview
description: Generate Mermaid diagram preview URLs for mermaid.live. Use when the user asks to preview, share, or create a link for a Mermaid diagram. Encodes Mermaid diagram code into a clickable mermaid.live/edit URL using pako (zlib) compression + URL-safe base64 encoding.
---

# Mermaid Live Preview

Generate shareable preview URLs for Mermaid diagrams on [mermaid.live](https://mermaid.live).

## How It Works

The Mermaid Live Editor encodes diagram state into the URL hash using:
1. **JSON** wrapping the diagram code and config into a `State` object
2. **zlib compression** (level 9, standard zlib with `78 DA` header)
3. **URL-safe base64** encoding (no padding)
4. **`#pako:` prefix** in the URL fragment

This skill provides `scripts/encode.py` to perform this encoding/decoding.

## Workflows

### Generate a Preview URL

When the user has Mermaid diagram code (either inline, in a file, or generated during the conversation):

```bash
python3 scripts/encode.py "graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[OK]
    B -->|No| D[Cancel]"
```

Or pipe from a `.mmd` file:

```bash
python3 scripts/encode.py < diagram.mmd
```

The script outputs two URLs:
- **Edit**: `https://mermaid.live/edit#pako:...` — opens the editor with the diagram, user can modify
- **View**: `https://mermaid.live/view#pako:...` — read-only preview, clean presentation for sharing

Present both to the user as clickable markdown links.

### Decode an Existing URL

When the user provides a mermaid.live URL and wants to see the source code:

```bash
python3 scripts/encode.py --decode "https://mermaid.live/edit#pako:..."
```

### End-to-End Example

1. User asks to create a sequence diagram and preview it
2. Write the Mermaid code
3. Run `encode.py` with the code to get the URL
4. Present both URLs to the user:
   - `[Edit on Mermaid Live](https://mermaid.live/edit#pako:...)`
   - `[Preview on Mermaid Live](https://mermaid.live/view#pako:...)`

## Supported Diagram Types

All Mermaid diagram types are supported, including:
- Flowcharts (`graph TD`, `graph LR`)
- Sequence diagrams (`sequenceDiagram`)
- Class diagrams (`classDiagram`)
- State diagrams (`stateDiagram-v2`)
- Entity-Relationship (`erDiagram`)
- Gantt charts (`gantt`)
- Pie charts (`pie`)
- Gitgraph (`gitGraph`)
- Mindmaps (`mindmap`)
- Timeline (`timeline`)

## Theme Options

The default theme is `"default"`. You can modify `encode.py` to use other Mermaid themes:
- `default` - Standard theme
- `dark` - Dark mode
- `forest` - Green tones
- `neutral` - Grayscale

## Guidelines

- Always present both edit and view URLs as clickable markdown links
- For large diagrams, write the code to a `.mmd` file first, then pipe it to `encode.py`
- The script requires only Python 3 standard library (no pip installs needed)
- If the user provides a mermaid.live URL, decode it first to understand the diagram before making modifications
