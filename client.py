"""
MCP Direct Client — calls tools directly (no LLM tool-calling needed)
Uses Ollama only for the final summarization step, after we've fetched real data.
100% FREE, no API key required.
"""

import asyncio
import requests
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "mistral"


def ask_ollama(prompt: str) -> str:
    """Send a plain text prompt to Ollama and return the response."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json().get("message", {}).get("content", "").strip()


async def main():
    print("=" * 55)
    print("  MCP Direct Client (100% FREE, runs locally)")
    print("=" * 55)

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ MCP server connected!\n")

            # ── Step 1: List all files ────────────────────────────────────────
            print("🔧 Calling tool: list_files")
            result = await session.call_tool("list_files", {})
            list_output = result.content[0].text if result.content else ""
            print(f"   ↳ {list_output}\n")

            # Parse filenames from the output
            filenames = [
                line.strip().lstrip("- ").strip()
                for line in list_output.splitlines()
                if line.strip().startswith("-")
            ]

            if not filenames:
                print("No files found. Add .txt files to the my_files/ folder.")
                return

            # ── Step 2: Read each file ────────────────────────────────────────
            file_contents = {}
            for filename in filenames:
                print(f"🔧 Calling tool: read_file  →  {filename}")
                result = await session.call_tool("read_file", {"filename": filename})
                content = result.content[0].text if result.content else ""
                file_contents[filename] = content
                preview = content[:120] + ("..." if len(content) > 120 else "")
                print(f"   ↳ {preview}\n")

            # ── Step 3: Send real content to Ollama for summarization ─────────
            print("⏳ Sending real file contents to Ollama for summary...\n")

            combined = "\n\n".join(
                f"=== {name} ===\n{body}"
                for name, body in file_contents.items()
            )

            prompt = (
                f"Here are the actual contents of {len(file_contents)} files:\n\n"
                f"{combined}\n\n"
                f"Please write a short, clear summary of each file based strictly "
                f"on the content above. Do not add anything that isn't in the files."
            )

            summary = ask_ollama(prompt)
            print(f"🤖 AI Summary:\n\n{summary}\n")

    print("=" * 55)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())