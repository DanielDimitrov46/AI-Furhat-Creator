from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

def gen_id() -> str:
    return str(uuid.uuid4())

class Character(Base):
    __tablename__ = "characters"

    id = Column(String, primary_key=True, default=gen_id)
    name = Column(String, nullable=False)
    short_description = Column(Text, nullable=True)
    character_prompt = Column(Text, nullable=False)
    language = Column(String, nullable=False, default="en")
    voice_id = Column(String, nullable=True)
    face_id = Column(String, nullable=True)
    max_turns = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="character")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=gen_id)
    character_id = Column(String, ForeignKey("characters.id"), nullable=False)
    user_id = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")  # active|ended
    created_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    character = relationship("Character", back_populates="sessions")
    turns = relationship("Turn", back_populates="session")

class Turn(Base):
    __tablename__ = "turns"

    id = Column(String, primary_key=True, default=gen_id)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    speaker = Column(String, nullable=False)  # user|character
    text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="turns")
