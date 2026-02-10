
import os
from pathlib import Path
from dotenv import load_dotenv

from fastmcp import FastMCP
from google import genai

# ---------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set GOOGLE_API_KEY in .env")

# ---------------------------------------------------------------------
# Gemini client (NEW SDK)
# ---------------------------------------------------------------------
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

# ---------------------------------------------------------------------
# FastMCP Server
# ---------------------------------------------------------------------
mcp = FastMCP("tour-food")


@mcp.tool()
def top_food_to_try(city: str) -> str:
    """
    Returns top local foods for a city using Gemini.
    This tool is dynamically generated (no hardcoded content).
    """

    # 🔥 HARD PROOF TOOL WAS CALLED
    print(f"🛠 MCP TOOL EXECUTED → top_food_to_try(city='{city}')")

    prompt = f"""
You are a local food expert.

City: {city}

Task:
List 8–10 iconic local foods or drinks people must try in this city.

Rules:
- Use bullet points
- For each item include:
  - Food name
  - Short description
  - Typical place or time locals eat it
- No JSON
- No markdown headings
- No emojis
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip() if response.text else ""

        if not text:
            return "⚠️ Food data could not be generated at the moment."

        # 🧪 TOOL SIGNATURE (DEBUG ONLY — REMOVE IN PROD IF YOU WANT)
        return f"[SOURCE: MCP_TOOL:tour-food]\n{text}"

    except Exception as e:
        return f"❌ Tool execution failed: {str(e)}"


# ---------------------------------------------------------------------
# Run server
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # STDIO by default
    # For HTTP:
    # fastmcp run servers/food_server.py:mcp --transport http --port 8002
    mcp.run()
