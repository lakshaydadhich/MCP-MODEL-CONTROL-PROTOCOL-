
import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from fastmcp import FastMCP

# ---- Load .env (project root) ----
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# ---- Gemini init ------------------------------------------------------------
GEMINI_MODEL = "models/gemini-2.5-flash"

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError(
        "Please set GOOGLE_API_KEY environment variable before starting places_server."
    )

genai.configure(api_key=api_key)
model = genai.GenerativeModel(GEMINI_MODEL)


# ---- FastMCP server ---------------------------------------------------------

mcp = FastMCP("tour-places")


@mcp.tool
def top_places_to_visit(city: str) -> str:
    """
    List the top 8–10 places to visit in a city.

    Returns a human-readable bullet list for LLM consumption.
    """
    prompt = (
        "You are a local travel expert.\n\n"
        f"City: {city}\n\n"
        "List the top 8–10 places to visit in this city. For each place, "
        "include: name, neighborhood/area (if relevant), and 1–2 sentence reason "
        "why it's worth visiting.\n\n"
        "Answer in clear bullet points, no JSON, no code."
    )

    response = model.generate_content(prompt)
    return response.text or ""


if __name__ == "__main__":
    # Default transport is stdio; for HTTP, run via FastMCP CLI, e.g.:
    #   fastmcp run servers/places_server.py:mcp --transport http --port 8001
    mcp.run()