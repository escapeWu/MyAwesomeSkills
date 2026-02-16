#!/usr/bin/env python3
"""
Encode Mermaid diagram code into a mermaid.live preview URL, or decode one back.

Usage:
    # Encode from stdin
    echo 'graph TD; A-->B' | python3 encode.py

    # Encode from file
    python3 encode.py < diagram.mmd

    # Encode inline
    python3 encode.py "graph TD; A-->B"

    # Decode a URL
    python3 encode.py --decode "https://mermaid.live/edit#pako:..."
"""

import base64
import json
import sys
import zlib


def encode(mermaid_code: str, theme: str = "default") -> str:
    """Encode Mermaid source code into a pako base64 payload."""
    state = {
        "code": mermaid_code,
        "mermaid": json.dumps({"theme": theme}, indent=2),
        "updateDiagram": True,
        "rough": False,
        "panZoom": True,
        "grid": True,
    }
    json_bytes = json.dumps(state).encode("utf-8")
    compressed = zlib.compress(json_bytes, 9)
    b64 = base64.urlsafe_b64encode(compressed).rstrip(b"=").decode("ascii")
    return b64


def edit_url(mermaid_code: str, theme: str = "default") -> str:
    """Return a mermaid.live edit URL."""
    return f"https://mermaid.live/edit#pako:{encode(mermaid_code, theme)}"


def view_url(mermaid_code: str, theme: str = "default") -> str:
    """Return a mermaid.live view (read-only preview) URL."""
    return f"https://mermaid.live/view#pako:{encode(mermaid_code, theme)}"


def decode(url: str) -> str:
    """Decode a mermaid.live URL back to the Mermaid source code."""
    if "#pako:" not in url:
        raise ValueError("URL does not contain a #pako: fragment")
    payload = url.split("#pako:", 1)[1]
    # Restore base64 padding
    padding = 4 - len(payload) % 4
    if padding != 4:
        payload += "=" * padding
    compressed = base64.urlsafe_b64decode(payload)
    json_str = zlib.decompress(compressed).decode("utf-8")
    state = json.loads(json_str)
    return state.get("code", "")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--decode":
        if len(sys.argv) < 3:
            print("Usage: encode.py --decode <url>", file=sys.stderr)
            sys.exit(1)
        code = decode(sys.argv[2])
        print(code)
    elif len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        # Inline mermaid code as argument
        print(f"Edit: {edit_url(sys.argv[1])}")
        print(f"View: {view_url(sys.argv[1])}")
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("Usage: echo 'graph TD; A-->B' | python3 encode.py", file=sys.stderr)
            print("       python3 encode.py --decode <url>", file=sys.stderr)
            sys.exit(1)
        code = sys.stdin.read()
        print(f"Edit: {edit_url(code)}")
        print(f"View: {view_url(code)}")


if __name__ == "__main__":
    main()
