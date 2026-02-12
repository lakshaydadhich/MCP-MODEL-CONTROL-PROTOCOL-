🌍 Travel MCP Chatbot with Text-to-Speech (TTS)

A real-time Travel Assistant built using Model Context Protocol (MCP) with dynamic tool calling and integrated Text-to-Speech (TTS) functionality.

This project demonstrates:

🔧 Real MCP tool calling

🧠 LLM-based intent detection

🏨 Dynamic travel recommendations

🔊 Automatic audio generation of responses

📁 Organized modular architecture

🚀 Features
✅ MCP Tool Calling

The chatbot automatically detects user intent and calls the appropriate tool:

top_places_to_visit(city)

top_food_to_try(city)

top_hotels(city)

✅ Real Tool Execution

No hardcoded responses — tools execute real logic from individual MCP servers.

✅ Text-to-Speech (TTS)

Converts final chatbot response to speech

Cleans markdown symbols before speaking

Saves audio files inside the /output directory

Generates unique timestamp-based filenames

Produces .mp3 files

📂 Project Structure
CURSOR/
│
├── client/
│   ├── mcp_client.py      # Main MCP client logic
│   ├── tts.py             # Text-to-Speech module
│
├── servers/
│   ├── food_server.py     # Food recommendation MCP server
│   ├── hotels_server.py   # Hotels recommendation MCP server
│   ├── places_server.py   # Tourist places MCP server
│
├── output/                # Generated audio files (.mp3)
│
├── venv/                  # Virtual environment (optional)
├── .env                   # Environment variables
├── mcp.json               # MCP configuration
├── requirements.txt
└── README.md

🧠 How It Works
System Architecture
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

⚙️ Installation Guide
1️⃣ Clone the Repository
git clone <your-repository-url>
cd CURSOR

2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt


If TTS package is not included:

pip install gtts

4️⃣ Setup Environment Variables

Create a .env file in the root directory:

GOOGLE_API_KEY=your_api_key_here


If using:

Ollama

Groq

Gemini

Custom LLM proxy

Update configuration inside mcp_client.py accordingly.

▶️ Running the Application

Run the MCP client:

python client/mcp_client.py

💬 Example Usage
You: Top attractions in Jaipur

🔧 MCP TOOL CALLED → top_places_to_visit (city=Jaipur)

🤖 Here are the top places to visit in Jaipur...

🔊 Audio saved at: output/response_20260212_154210.mp3


The generated audio file will be stored in:

output/

🔊 Text-to-Speech (TTS) Details

The TTS module:

Cleans markdown symbols (*, **, bullet points)

Converts text into natural speech format

Generates .mp3 audio files

Automatically creates /output directory if missing

Uses timestamp-based unique filenames

Example generated file:

output/response_20260212_154210.mp3

🛠 Technology Stack

Python

MCP (Model Context Protocol)

FastMCP

Google Gemini / Ollama / Groq (configurable)

gTTS (Google Text-to-Speech)

FastAPI (if used in servers)

python-dotenv

📌 Key Highlights

Modular MCP server architecture

Clean separation of client and tool servers

Scalable for adding new tools

Easily extendable to:

Speech-to-Text (Whisper)

RAG Integration

Streamlit UI

Real Travel APIs

Voice Assistant Mode

🔮 Future Improvements

🎤 Add Speech-to-Text (Voice Input)

🌍 Multi-language support

🔊 Stream audio in real-time instead of saving

🌐 Streamlit Web UI

🧠 Add RAG for knowledge grounding

🗺 Integrate live travel APIs

☁ Deploy on cloud (AWS / GCP / Azure)

👨‍💻 Author

Lakshay Dadhich
B.Tech Computer Science (2024) – SKIT Jaipur
Data Science & AI Enthusiast

📜 License

This project is intended for educational and development purposes.
You are free to modify and expand it.