# import os
# from pathlib import Path

# from dotenv import load_dotenv
# import google.generativeai as genai
# from fastmcp import FastMCP

# # ---- Load .env (project root) ----
# load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# # ---- Gemini init ----
# GEMINI_MODEL = "models/gemini-2.5-flash"

# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     raise RuntimeError(
#         "Please set GOOGLE_API_KEY environment variable before starting food_server."
#     )

# genai.configure(api_key=api_key)
# model = genai.GenerativeModel(GEMINI_MODEL)


# # ---- FastMCP server ---------------------------------------------------------

# mcp = FastMCP("tour-food")


# @mcp.tool
# def top_food_to_try(city: str) -> str:
#     """
#     Use Gemini to get iconic local dishes/foods to try in a city.

#     Returns a human-readable bullet list for LLM consumption.
#     """
#     prompt = (
#         "You are a foodie travel expert.\n\n"
#         f"City: {city}\n\n"
#         "List the top 8–10 must-try local dishes, snacks, or drinks in this city. "
#         "For each item, include: name, what it is, and where/when locals typically eat it "
#         "(e.g. street food, breakfast pastry, late-night snack, etc.).\n\n"
#         "Answer in clear bullet points, no JSON, no code."
#     )

#     response = model.generate_content(prompt)
#     return response.text or ""


# if __name__ == "__main__":
#     # Default transport is stdio; for HTTP, run via FastMCP CLI, e.g.:
#     #   fastmcp run servers/food_server.py:mcp --transport http --port 8002
#     mcp.run()

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
