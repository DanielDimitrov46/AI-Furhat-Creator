from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas

def create_character(db: Session, data: schemas.CharacterCreate) -> models.Character:
    obj = models.Character(
        name=data.name,
        short_description=data.short_description,
        character_prompt=data.character_prompt,
        language=data.language,
        voice_id=data.voice_id,
        face_id=data.face_id,
        updated_at=datetime.utcnow(),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_characters(db: Session):
    return db.query(models.Character).all()

def get_character(db: Session, character_id: str):
    return db.query(models.Character).filter(models.Character.id == character_id).first()

def create_session(db: Session, character_id: str, user_id: str | None):
    obj = models.Session(character_id=character_id, user_id=user_id, status="active")
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_session(db: Session, session_id: str):
    return db.query(models.Session).filter(models.Session.id == session_id).first()

def end_session(db: Session, sess: models.Session):
    sess.status = "ended"
    sess.ended_at = datetime.utcnow()
    db.commit()
    db.refresh(sess)
    return sess

def create_turn(db: Session, session_id: str, speaker: str, text: str | None):
    obj = models.Turn(session_id=session_id, speaker=speaker, text=text)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_turns(db: Session, session_id: str):
    return (
        db.query(models.Turn)
        .filter(models.Turn.session_id == session_id)
        .order_by(models.Turn.created_at.asc())
        .all()
    )
