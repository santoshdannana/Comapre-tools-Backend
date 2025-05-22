import json
import re
from schemas.request_response import AskResponse, Solution
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.0-flash")


PROMPT_TEMPLATE = """
You are an AI research assistant. A user has asked: "{question}"

Search online and suggest 3-5 possible tools, frameworks, or platforms that solve the problem.

For each solution, return:
- Name
- Short description
- Pros (list)
- Cons (list)
- Pricing info
- Official website link

Respond only in valid **JSON format** as a list of objects. Do not include markdown like ```json.
"""

async def get_solutions(question: str) -> AskResponse:
    prompt = PROMPT_TEMPLATE.format(question=question)
    response = model.generate_content(prompt)

    try:
        raw = response.text.strip()

        # Remove markdown wrapper (```json ... ```)
        cleaned = re.sub(r"```json|```", "", raw).strip()

        json_data = json.loads(cleaned)

        # Normalize keys to match Pydantic model
        def normalize(item):
            return Solution(
                name=item.get("Name", "").strip(),
                description=item.get("Short description", "").strip(),
                pros=item.get("Pros", []),
                cons=item.get("Cons", []),
                pricing=item.get("Pricing info", "").strip(),
                link=item.get("Official website link", "").strip()
            )

        solutions = [normalize(item) for item in json_data]

        return AskResponse(question=question, solutions=solutions)

    except Exception as e:
        raise RuntimeError(f"Gemini parsing failed: {e}\nRaw Output:\n{response.text}")
