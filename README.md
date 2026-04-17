# MCP File Reader
A fully local, free AI-powered file reader that uses **MCP (Model Context Protocol)** to connect a Python tool server with a local LLM (Ollama + Mistral). No API keys, no cloud, no cost — runs entirely on your machine.

## 🧾 Features
- MCP Server with custom tools (`list_files`, `read_file`)
- Local LLM integration via Ollama (Mistral / Llama3.2)
- Automatic file discovery and content reading
- AI-powered summarization of file contents
- Path traversal protection (security built-in)
- Zero cost — no API keys or subscriptions required

## 🛠️ Tech Stack

| Technology | Description                              |
|------------|------------------------------------------|
| Python     | Core language for server and client      |
| MCP        | Model Context Protocol (tool server)     |
| Ollama     | Local LLM runtime (free, offline)        |
| Mistral    | Local AI model for summarization         |
| asyncio    | Async communication between client/server|
| requests   | HTTP calls to Ollama API                 |

## 📦 Installation

```bash
git clone https://github.com/JaneKarunyaJ/MCP-File-Reader.git
cd MCP-File-Reader
pip install mcp requests
```

Install Ollama from [https://ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull mistral
```

## 🚀 Usage

Make sure Ollama is running (it starts automatically after installation), then:

```bash
python client.py
```

The client will:
1. Launch the MCP server as a subprocess
2. Call `list_files` to discover files in `my_files/`
3. Call `read_file` for each file found
4. Send the real content to Mistral for summarization

## 📁 Project Structure

```
MCP-File-Reader/
│
├── server.py          # MCP server — exposes list_files and read_file tools
├── client.py          # MCP client — calls tools and queries Ollama
├── requirements.txt   # Python dependencies
└── my_files/          # Folder the AI is allowed to read
    ├── project_ideas.txt
    └── wishlist.txt
```

## 🔐 Security

- The MCP server only allows reads from the `my_files/` directory
- Path traversal attacks (e.g. `../../etc/passwd`) are automatically blocked
- No data leaves your machine — fully offline after setup

## 🧠 How It Works

```
client.py
   │
   ├── Step 1: Calls MCP tool → list_files()
   │              ↓
   │         Returns filenames from my_files/
   │
   ├── Step 2: Calls MCP tool → read_file(filename)
   │              ↓
   │         Returns actual file contents
   │
   └── Step 3: Sends real content to Ollama (Mistral)
                  ↓
             Returns AI summary
```

## ➕ Extending the Project

- **Add your own files**: Drop any `.txt` file into `my_files/` and run again
- **Add new tools**: Add a new tool handler in `server.py` (e.g. `search_in_file`, `write_file`)
- **Change the question**: Edit `user_question` in `client.py` to ask anything about your files
- **Swap the model**: Change `MODEL = "mistral"` in `client.py` to any model you have pulled in Ollama

## 📋 Requirements

- Python 3.9+
- Ollama installed ([ollama.com](https://ollama.com))
- Mistral model pulled (`ollama pull mistral`)
- `mcp` and `requests` Python packages
