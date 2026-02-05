from typing import List, Dict, Any

async def generate_turn(character_prompt: str, history: List[Dict[str, str]], user_text: str) -> Dict[str, Any]:
    # MVP stub: връща контролируем JSON без външен API
    return {
        "reply": f"(stub) You said: {user_text}",
        "facial_expression": {"label": "neutral"},
        "head_movement": {"label": "still"},
        "actions": []
    }
