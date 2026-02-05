from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class CharacterBase(BaseModel):
    name: str
    short_description: Optional[str] = None
    character_prompt: str
    language: str = "en"
    voice_id: Optional[str] = None
    face_id: Optional[str] = None

class CharacterCreate(CharacterBase):
    pass

class CharacterOut(CharacterBase):
    id: str
    max_turns: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SessionCreate(BaseModel):
    user_id: Optional[str] = None

class SessionOut(BaseModel):
    id: str
    character_id: str
    user_id: Optional[str] = None
    status: str
    created_at: datetime
    ended_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserTurnIn(BaseModel):
    text: str

class CharacterTurnOut(BaseModel):
    text: str
    facial_expression: Dict[str, Any]
    head_movement: Dict[str, Any]
    actions: List[Dict[str, Any]]
