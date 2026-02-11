# import asyncio
# import json
# import os
# import re
# from pathlib import Path
# from typing import Dict, Any

# from dotenv import load_dotenv
# from fastmcp import Client
# from google import genai

# # ---------------------------------------------------------------------
# # ENV
# # ---------------------------------------------------------------------

# load_dotenv()
# API_KEY = os.getenv("GOOGLE_API_KEY")
# if not API_KEY:
#     raise RuntimeError("GOOGLE_API_KEY not set")

# MODEL_NAME = "gemini-2.5-flash"
# llm = genai.Client(api_key=API_KEY)

# # ---------------------------------------------------------------------
# # PATHS (✔ CORRECT)
# # ---------------------------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parents[1]   # cursor/
# CONFIG_PATH = BASE_DIR / "mcp.json"

# # ---------------------------------------------------------------------
# # CONFIG
# # ---------------------------------------------------------------------

# def load_config(path: Path) -> Dict[str, Any]:
#     if not path.exists():
#         raise FileNotFoundError(f"Config file not found: {path}")
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)

# # ---------------------------------------------------------------------
# # HELPERS
# # ---------------------------------------------------------------------

# def is_greeting(text: str) -> bool:
#     return text.lower().strip() in {"hi", "hello", "hey", "hii", "hlo"}

# def fallback_tool(text: str) -> str | None:
#     t = text.lower()
#     if "food" in t:
#         return "top_food_to_try"
#     if "place" in t or "visit" in t or "tourist" in t:
#         return "top_places_to_visit"
#     if "hotel" in t or "stay" in t:
#         return "top_hotels_to_stay"
#     return None

# def fallback_city(text: str) -> str | None:
#     blacklist = {"food", "items", "places", "visit", "tourist", "hotel", "stay"}
#     words = re.findall(r"[a-zA-Z]+", text.lower())
#     for w in words:
#         if w not in blacklist and len(w) > 3:
#             return w.capitalize()
#     return None

# # ---------------------------------------------------------------------
# # INTENT PARSER (NO JSON MODE — STABLE)
# # ---------------------------------------------------------------------

# def parse_intent(question: str) -> dict:
#     prompt = f"""
# Extract city and intent from the user query.

# Query: {question}

# Reply in plain text format:
# city=<city or NONE>
# intent=<food|places|hotels|NONE>
# """

#     try:
#         response = llm.models.generate_content(
#             model=MODEL_NAME,
#             contents=prompt
#         )

#         text = response.text.lower() if response.text else ""
#         city = fallback_city(question)

#         if "food" in text:
#             tool = "top_food_to_try"
#         elif "place" in text or "visit" in text:
#             tool = "top_places_to_visit"
#         elif "hotel" in text or "stay" in text:
#             tool = "top_hotels_to_stay"
#         else:
#             tool = fallback_tool(question)

#         return {"city": city, "tool": tool}

#     except Exception:
#         return {
#             "city": fallback_city(question),
#             "tool": fallback_tool(question)
#         }

# # ---------------------------------------------------------------------
# # MCP CALL
# # ---------------------------------------------------------------------

# async def call_tool(server_url: str, tool: str, payload: dict) -> str:
#     async with Client(server_url) as c:
#         result = await c.call_tool(tool, payload)

#     return "\n".join(
#         block.text for block in result.content
#         if hasattr(block, "text") and block.text
#     )

# # ---------------------------------------------------------------------
# # MAIN LOOP
# # ---------------------------------------------------------------------

# async def main():
#     config = load_config(CONFIG_PATH)

#     tool_to_server = {
#         tool: server["url"]
#         for server in config["servers"]
#         for tool in server["tools"]
#     }

#     print("\n🤖 Travel MCP Chatbot (type 'exit' to quit)\n")

#     while True:
#         q = input("You: ").strip()
#         if q.lower() in {"exit", "quit"}:
#             break

#         if is_greeting(q):
#             print("\n🤖 Hi! Ask about food, places, or hotels in any city.\n")
#             continue

#         intent = parse_intent(q)
#         city, tool = intent["city"], intent["tool"]

#         if not city or not tool:
#             print("\n🤖 Please ask a tool specific question.\n")
#             continue

#         print(f"\n🔧 MCP TOOL CALLED → {tool} (city={city})")

#         try:
#             result = await call_tool(tool_to_server[tool], tool, {"city": city})
#             print("\n🤖", result, "\n")
#         except Exception as e:
#             print(f"\n❌ Tool error: {e}\n")

# # ---------------------------------------------------------------------

# if __name__ == "__main__":
#     asyncio.run(main())








import asyncio
import json
import os
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from fastmcp import Client
from google import genai
from google.genai import types

# ---------------------------------------------------------------------
# ENV & PATHS
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "mcp.json"

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set")

# MODEL_NAME = "gemini-2.5-flash"
MODEL_NAME = "gemini-2.5-flash-lite"
llm = genai.Client(api_key=API_KEY)

# ---------------------------------------------------------------------
# CONFIG LOADER
# ---------------------------------------------------------------------

def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------------------
# INTENT PARSER (NO HARDCODED WORDS)
# ---------------------------------------------------------------------

def parse_intent(question: str) -> dict:
    prompt = f"""
You are a strict intent extraction system.

Extract:
- city: a real geographic city explicitly mentioned by the user
- tool: the best matching tool

Allowed tools:
- top_food_to_try
- top_places_to_visit
- top_hotels_to_stay

Rules:
- Do not guess
- Do not infer missing data
- If city is not explicit, return null
- If no tool applies, return null
- Output JSON only
- No explanations

User query:
{question}

Return JSON:
{{
  "city": string | null,
  "tool": string | null
}}
"""

    try:
        response = llm.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0
            )
        )

        text = (response.text or "").strip()
        return json.loads(text)

    except Exception as e:
        print(f"⚠️ Intent parsing failed: {e}")
        return {"city": None, "tool": None}

# ---------------------------------------------------------------------
# PURE STRUCTURAL VALIDATION
# ---------------------------------------------------------------------

def is_valid_city(city: Any) -> bool:
    return isinstance(city, str) and city.strip() != ""

def is_valid_tool(tool: Any, allowed: set) -> bool:
    return tool in allowed

# ---------------------------------------------------------------------
# MCP TOOL CALL
# ---------------------------------------------------------------------

async def call_tool(server_url: str, tool: str, payload: dict) -> str:
    async with Client(server_url) as client:
        result = await client.call_tool(tool, payload)

    outputs = []
    for block in result.content:
        if hasattr(block, "text") and block.text:
            outputs.append(block.text)

    return "\n".join(outputs)

# ---------------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------------

async def main():
    config = load_config(CONFIG_PATH)

    tool_to_server = {}
    for server in config["servers"]:
        for tool in server["tools"]:
            tool_to_server[tool] = server["url"]

    allowed_tools = set(tool_to_server.keys())

    print("\n🤖 Travel MCP Chatbot")
    print("Ask about food, places, or hotels in any city.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("\n👋 Goodbye!")
            break

        intent = parse_intent(query)
        city = intent.get("city")
        tool = intent.get("tool")

        if not is_valid_tool(tool, allowed_tools):
            print("\n🤖 I couldn't determine what you want to explore.\n")
            continue

        if not is_valid_city(city):
            print("\n🤖 I couldn't find a city in your question.\n")
            continue

        print(f"\n🔧 MCP TOOL CALLED → {tool} (city={city})")

        try:
            result = await call_tool(
                tool_to_server[tool],
                tool,
                {"city": city}
            )
            print("\n🤖", result, "\n")

        except Exception as e:
            print(f"\n❌ Tool execution failed: {e}\n")

# ---------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())



