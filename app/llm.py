import json
import os
from dotenv import load_dotenv
from typing import List, Dict
from openai import AsyncOpenAI
from openai import RateLimitError
from app.knowledge import retrieve_knowledge

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

BASE_SYSTEM_PROMPT = """
You are an embodied conversational robot.

Always respond ONLY in JSON format.

{
  "reply": string,
  "facial_expression": { "label": string },
  "head_movement": { "label": string },
  "actions": []
}

Do not output anything outside JSON.
"""


def build_messages(character_prompt: str, history: List[Dict], knowledge: str):

    messages = [
        {"role": "system", "content": BASE_SYSTEM_PROMPT},
        {"role": "system", "content": f"Character personality:\n{character_prompt}"}
    ]

    if knowledge:
        messages.append({
            "role": "system",
            "content": f"Knowledge context:\n{knowledge}"
        })

    messages.extend(history)

    return messages


async def call_llm(messages):

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content

    except RateLimitError:
        return None

def validate_response(raw):

    try:
        parsed = json.loads(raw)

        if "reply" not in parsed:
            parsed["reply"] = ""

        if "facial_expression" not in parsed:
            parsed["facial_expression"] = {"label": "neutral"}

        if "head_movement" not in parsed:
            parsed["head_movement"] = {"label": "still"}

        if "actions" not in parsed:
            parsed["actions"] = []

        return parsed

    except Exception:

        return {
            "reply": "Sorry, something went wrong.",
            "facial_expression": {"label": "neutral"},
            "head_movement": {"label": "still"},
            "actions": []
        }


async def generate_turn(character_prompt, history, character_id):

    knowledge = retrieve_knowledge(character_id)

    messages = build_messages(character_prompt, history, knowledge)

    raw = await call_llm(messages)

    if not raw:
        return {
            "reply": "The system is currently unavailable. Please try again later.",
            "facial_expression": {"label": "sad"},
            "head_movement": {"label": "shake"},
            "actions": []
        }