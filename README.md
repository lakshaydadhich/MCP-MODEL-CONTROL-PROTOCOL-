# 🌍 Travel MCP Chatbot with Text-to-Speech

> A real-time Travel Assistant built using **Model Context Protocol (MCP)** with dynamic tool calling and integrated Text-to-Speech (TTS) functionality.

---

## ✨ What This Project Demonstrates

| Capability | Description |
|---|---|
| 🔧 **Real MCP Tool Calling** | Detects user intent and routes to the right tool automatically |
| 🧠 **LLM-Based Intent Detection** | No hardcoded logic — the model decides |
| 🏨 **Dynamic Travel Recommendations** | Places, food, and hotels on demand |
| 🔊 **Auto Audio Generation** | Converts responses to `.mp3` speech |
| 📁 **Modular Architecture** | Clean separation of client, servers, and utilities |

---

## 🚀 Features

### ✅ MCP Tool Calling

The chatbot automatically detects user intent and calls the appropriate tool:

```
top_places_to_visit(city)
top_food_to_try(city)
top_hotels(city)
```

### ✅ Real Tool Execution

No hardcoded responses — tools execute real logic from individual MCP servers.

### ✅ Text-to-Speech (TTS)

- Converts final chatbot response to natural speech
- Cleans markdown symbols before speaking
- Saves `.mp3` audio files inside the `/output` directory
- Generates unique timestamp-based filenames

---

## 📂 Project Structure

```
CURSOR/
│
├── client/
│   ├── mcp_client.py          # Main MCP client logic
│   └── tts.py                 # Text-to-Speech module
│
├── servers/
│   ├── food_server.py         # Food recommendation MCP server
│   ├── hotels_server.py       # Hotels recommendation MCP server
│   └── places_server.py       # Tourist places MCP server
│
├── output/                    # Generated audio files (.mp3)
├── venv/                      # Virtual environment (optional)
│
├── .env                       # Environment variables
├── mcp.json                   # MCP configuration
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

```
User Input
    ↓
MCP Client
    ↓
LLM Intent Detection
    ↓
Tool Call (Places / Food / Hotels)
    ↓
MCP Server Execution
    ↓
Final Text Response
    ↓
TTS Module
    ↓
Audio Saved in /output
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd CURSOR
```

### 2️⃣ Create Virtual Environment *(Optional but Recommended)*

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If TTS package is not included:

```bash
pip install gtts
```

### 4️⃣ Setup Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_api_key_here
```

> **Note:** If using Ollama, Groq, Gemini, or a custom LLM proxy — update the configuration inside `mcp_client.py` accordingly.

---

## ▶️ Running the Application

```bash
python client/mcp_client.py
```

---

## 💬 Example Usage

```
You: Top attractions in Jaipur

🔧 MCP TOOL CALLED → top_places_to_visit (city=Jaipur)

🤖 Here are the top places to visit in Jaipur...

🔊 Audio saved at: output/response_20260212_154210.mp3
```

Generated audio files are stored in:

```
output/response_<YYYYMMDD_HHMMSS>.mp3
```

---

## 🔊 Text-to-Speech (TTS) Details

The TTS module:

- Cleans markdown symbols (`*`, `**`, bullet points)
- Converts text into natural speech format
- Generates `.mp3` audio files
- Auto-creates `/output` directory if missing
- Uses timestamp-based unique filenames

**Example output file:**
```
output/response_20260212_154210.mp3
```

---

## 🛠 Technology Stack

| Technology | Role |
|---|---|
| **Python** | Core language |
| **MCP / FastMCP** | Model Context Protocol framework |
| **Google Gemini / Ollama / Groq** | LLM backend (configurable) |
| **gTTS** | Google Text-to-Speech |
| **FastAPI** | Server transport (optional) |
| **python-dotenv** | Environment variable management |

---

## 📌 Key Highlights

- **Modular MCP server architecture** — each tool lives in its own server
- **Clean client/server separation** — easy to maintain and extend
- **Scalable** — add new tools without touching existing ones
- **Extensible** — ready for STT, RAG, Streamlit, and live API integrations

---

## 🔮 Future Improvements

- 🎤 **Speech-to-Text** — Voice input via Whisper
- 🌍 **Multi-language support** — Serve global travelers
- 🔊 **Real-time audio streaming** — No need to save files first
- 🌐 **Streamlit Web UI** — Friendly browser interface
- 🧠 **RAG Integration** — Ground responses in curated travel knowledge
- 🗺 **Live Travel APIs** — Real hotels, prices, and availability
- ☁️ **Cloud Deployment** — AWS / GCP / Azure ready

---

## 👨‍💻 Author

**Lakshay Dadhich**
B.Tech Computer Science (2024) — SKIT Jaipur
Data Science & AI Enthusiast

---

## 📜 License

This project is intended for **educational and development purposes**.
You are free to modify and expand it.
