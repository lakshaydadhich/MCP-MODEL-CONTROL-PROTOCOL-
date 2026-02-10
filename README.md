🧳 Travel MCP Chatbot (Gemini + FastMCP)

A dynamic Travel Chatbot built using Model Context Protocol (MCP), FastMCP, and Google Gemini.
The chatbot intelligently decides whether to answer directly from the LLM or call the appropriate MCP tool (food, hotels, places) — no hardcoded responses.

✨ Features

🤖 Natural language chatbot (Gemini LLM)

🔧 Real tool calling via MCP

🏙️ Ask about:

Top tourist places

Famous food

Best hotels

🧠 Automatic decision:

Tool response → MCP Server

General chat → LLM

🧩 Modular MCP server design

🧪 Easy to verify whether response came from LLM or Tool

📁 Project Structure
cursor/
│
├── client/
│   └── mcp_client.py          # Chatbot client (LLM + MCP integration)
│
├── servers/
│   ├── food_server.py         # Food-related MCP tools
│   ├── hotels_server.py       # Hotel-related MCP tools
│   └── places_server.py       # Tourist places MCP tools
│
├── venv/                      # Virtual environment
│
├── .env                       # API keys (ignored in git)
├── mcp.json                   # MCP server configuration
├── requirement.txt            # Python dependencies
├── test_gemini.py             # Gemini API test script
└── README.md

🧠 How It Works (Architecture)
User Question
     ↓
mcp_client.py
     ↓
Gemini LLM
     ↓
┌───────────────┐
│ Tool Needed ? │
└───────┬───────┘
        │ Yes
        ↓
   MCP Server
 (food / hotels / places)
        ↓
   Tool Response
        ↓
   Final Answer


Gemini decides which tool to call

MCP executes the tool

Result is sent back to Gemini

Gemini formats the final response

🛠️ Tech Stack

Python 3.10+

Google Gemini (google-generativeai)

FastMCP

AsyncIO

dotenv

📦 Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/travel-mcp-chatbot.git
cd travel-mcp-chatbot

2️⃣ Create virtual environment
python -m venv venv


Activate:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirement.txt

🔐 Environment Setup

Create a .env file in the root directory:

GOOGLE_API_KEY=your_gemini_api_key_here


⚠️ Do not commit .env to GitHub

⚙️ MCP Configuration (mcp.json)

Example:

{
  "mcpServers": {
    "food": {
      "command": "python",
      "args": ["servers/food_server.py"]
    },
    "hotels": {
      "command": "python",
      "args": ["servers/hotels_server.py"]
    },
    "places": {
      "command": "python",
      "args": ["servers/places_server.py"]
    }
  }
}

🚀 Running the Chatbot
Step 1: Start the chatbot client
cd client
python mcp_client.py


You’ll see:

🤖 Travel MCP Chatbot (type 'exit' to quit)

💬 Example Conversations
Tool-based question (MCP is called)
You: top places to visit in jaipur

🔧 MCP TOOL CALLED → top_places_to_visit (city=Jaipur)

🤖 Amber Fort, Hawa Mahal, City Palace, Jantar Mantar...

LLM-only question (no tool)
You: hi

🤖 Hi! Ask about food, places, or hotels in any city.

🔍 How to Check Tool vs LLM Response
✅ Tool Response Indicators

Logs like:

🔧 MCP TOOL CALLED →


Data comes from servers/*.py

✅ LLM Response Indicators

No MCP log

Pure Gemini-generated text

This ensures no hardcoded logic.

🧪 Test Gemini Separately
python test_gemini.py


Used to confirm:

API key is valid

Gemini SDK is working

🧩 Adding New Tools (Example)

Create a new server:

servers/weather_server.py


Register tool using @tool

Add it to mcp.json

Restart chatbot — no client changes needed 🎯

❌ Common Issues & Fixes
❌ MCP connection failed

✔ Ensure:

MCP servers are correctly defined in mcp.json

Paths are correct

Python is activated inside venv

❌ Gemini JSON error

✔ Use:

model.generate_content(prompt)


✔ Avoid unsupported arguments like generation_config

📌 Future Enhancements

🌐 Real-time APIs (Google Places)

🖥️ Streamlit UI

🧠 RAG integration

🗣️ Voice-based input

🌍 Multi-language support

👨‍💻 Author

LAKSHAY DADHICH
Data Science | AI/ML | DATA ANALYTICS | LLM Systems