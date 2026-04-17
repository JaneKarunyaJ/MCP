"""
MCP File Reader Server
Exposes two tools: list_files and read_file
Run this as a subprocess via the client — do NOT run manually.
"""

import asyncio
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# ── Change this to any folder you want the AI to read from ──
ALLOWED_DIRECTORY = "./my_files"
# ────────────────────────────────────────────────────────────

app = Server("file-reader-server")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_files",
            description="List all files in the allowed directory.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="read_file",
            description="Read the contents of a specific file by name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file to read, e.g. 'notes.txt'",
                    }
                },
                "required": ["filename"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    base_dir = Path(ALLOWED_DIRECTORY).resolve()

    if name == "list_files":
        if not base_dir.exists():
            return [types.TextContent(type="text", text=f"Directory '{ALLOWED_DIRECTORY}' does not exist.")]
        files = [f.name for f in base_dir.iterdir() if f.is_file()]
        if not files:
            return [types.TextContent(type="text", text="No files found.")]
        result = "Files available:\n" + "\n".join(f"  - {f}" for f in sorted(files))
        return [types.TextContent(type="text", text=result)]

    elif name == "read_file":
        filename = arguments.get("filename", "")
        target = (base_dir / filename).resolve()
        # Security: block directory traversal
        if not str(target).startswith(str(base_dir)):
            return [types.TextContent(type="text", text="Error: Access denied.")]
        if not target.exists() or not target.is_file():
            return [types.TextContent(type="text", text=f"Error: File '{filename}' not found.")]
        try:
            content = target.read_text(encoding="utf-8")
            return [types.TextContent(type="text", text=f"Contents of '{filename}':\n\n{content}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error reading file: {e}")]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())