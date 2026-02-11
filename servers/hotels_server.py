import os
from pathlib import Path
from typing import Optional

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
        "Please set GOOGLE_API_KEY environment variable before starting hotels_server."
    )

genai.configure(api_key=api_key)
model = genai.GenerativeModel(GEMINI_MODEL)


# ---- FastMCP server ---------------------------------------------------------

mcp = FastMCP("tour-hotels")


@mcp.tool
def top_hotels_to_stay(city: str, budget_level: Optional[str] = None) -> str:
    """
    Call Gemini 2.5 to suggest areas and example hotels.

    budget_level: 'budget', 'midrange', or 'luxury' (optional).
    """
    budget = (budget_level or "midrange").lower()

    prompt = (
        "You are a hotel and neighborhood expert for travelers.\n\n"
        f"City: {city}\n"
        f"Budget level: {budget} (options: budget, midrange, luxury)\n\n"
        "1. Recommend 3–5 neighborhoods or areas that are great for visitors with this budget, "
        "explaining briefly why (e.g. close to sights, safe, nightlife, transport).\n"
        "2. For each area, suggest 1–2 example hotels or accommodation types suitable for this budget "
        "(you can invent realistic-sounding names if needed; they don't have to be real).\n\n"
        "Answer in bullet points grouped by neighborhood, no JSON, no code."
    )

    response = model.generate_content(prompt)

    return response.text or ""


if __name__ == "__main__":
    # Default transport is stdio; for HTTP, run via FastMCP CLI, e.g.:
    #   fastmcp run servers/hotels_server.py:mcp --transport http --port 8003
    mcp.run()


# import requests
# from fastmcp import FastMCP

# mcp = FastMCP("tour-hotels")


# @mcp.tool
# def top_hotels_to_stay(city: str) -> str:

#     print(f"🛠 REAL TOOL EXECUTED → top_hotels_to_stay(city='{city}')")

#     overpass_url = "https://overpass-api.de/api/interpreter"

#     headers = {
#         "User-Agent": "TravelMCPApp/1.0"
#     }

#     query = f"""
#     [out:json][timeout:25];
#     area["name"="{city}"]["boundary"="administrative"]->.searchArea;
#     (
#       node["tourism"="hotel"](area.searchArea);
#       node["tourism"="guest_house"](area.searchArea);
#     );
#     out body 8;
#     """

#     try:
#         response = requests.post(overpass_url, data=query, headers=headers, timeout=30)

#         response.raise_for_status()

#         data = response.json()
#         elements = data.get("elements", [])

#         hotels = []

#         for el in elements:
#             name = el.get("tags", {}).get("name")
#             if name:
#                 hotels.append(f"- {name}")

#         if not hotels:
#             return "⚠️ No hotels found."

#         return "\n".join(hotels)

#     except Exception as e:
#         return f"❌ Overpass error: {str(e)}"


# if __name__ == "__main__":
#     mcp.run()




