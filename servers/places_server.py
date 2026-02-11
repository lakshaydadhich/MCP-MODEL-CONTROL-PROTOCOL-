
import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from fastmcp import FastMCP

# ---- Load .env (project root) ----
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# ---- Gemini init ------------------------------------------------------------
# GEMINI_MODEL = "models/gemini-2.5-flash"
GEMINI_MODEL = "gemini-2.5-flash-lite"

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





# import requests
# from fastmcp import FastMCP

# mcp = FastMCP("tour-places")


# @mcp.tool
# def top_places_to_visit(city: str) -> str:
#     """
#     Fetch real tourist attractions using OpenStreetMap
#     """

#     print(f"🛠 REAL TOOL EXECUTED → top_places_to_visit(city='{city}')")

#     overpass_url = "https://overpass-api.de/api/interpreter"

#     query = f"""
#     [out:json];
#     area["name"="{city}"]->.searchArea;
#     (
#       node["tourism"="attraction"](area.searchArea);
#       node["historic"](area.searchArea);
#       node["tourism"="museum"](area.searchArea);
#     );
#     out body 10;
#     """

#     response = requests.post(overpass_url, data=query)

#     if response.status_code != 200:
#         return "❌ Failed to fetch attraction data."

#     data = response.json()
#     elements = data.get("elements", [])

#     places = []

#     for el in elements:
#         name = el.get("tags", {}).get("name")
#         if name:
#             places.append(f"- {name}")

#     if not places:
#         return "⚠️ No attractions found."

#     return "\n".join(places)


# if __name__ == "__main__":
#     mcp.run()
