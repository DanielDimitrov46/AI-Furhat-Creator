from typing import List, Dict
from sqlalchemy.orm import Session
from . import crud

def build_history(db: Session, session_id: str) -> List[Dict[str, str]]:
    turns = crud.list_turns(db, session_id)
    history: List[Dict[str, str]] = []
    for t in turns:
        role = "user" if t.speaker == "user" else "assistant"
        history.append({"role": role, "content": t.text or ""})
    return history
