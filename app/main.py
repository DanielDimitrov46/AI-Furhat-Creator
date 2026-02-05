from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import schemas, crud, llm, sessions as session_utils

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Furhat-like Creator Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/characters", response_model=schemas.CharacterOut)
def create_character(body: schemas.CharacterCreate, db: Session = Depends(get_db)):
    return crud.create_character(db, body)

@app.get("/characters", response_model=list[schemas.CharacterOut])
def list_characters(db: Session = Depends(get_db)):
    return crud.list_characters(db)

@app.get("/characters/{character_id}", response_model=schemas.CharacterOut)
def get_character(character_id: str, db: Session = Depends(get_db)):
    obj = crud.get_character(db, character_id)
    if not obj:
        raise HTTPException(404, "Character not found")
    return obj

@app.post("/characters/{character_id}/sessions", response_model=schemas.SessionOut)
def start_session(character_id: str, body: schemas.SessionCreate | None = None, db: Session = Depends(get_db)):
    char = crud.get_character(db, character_id)
    if not char:
        raise HTTPException(404, "Character not found")
    user_id = body.user_id if body else None
    return crud.create_session(db, character_id, user_id)

@app.post("/sessions/{session_id}/end", response_model=schemas.SessionOut)
def end_session(session_id: str, db: Session = Depends(get_db)):
    sess = crud.get_session(db, session_id)
    if not sess:
        raise HTTPException(404, "Session not found")
    return crud.end_session(db, sess)

@app.post("/sessions/{session_id}/user-turn", response_model=schemas.CharacterTurnOut)
async def user_turn(session_id: str, body: schemas.UserTurnIn, db: Session = Depends(get_db)):
    sess = crud.get_session(db, session_id)
    if not sess or sess.status != "active":
        raise HTTPException(400, "Session not active or not found")

    char = crud.get_character(db, sess.character_id)
    if not char:
        raise HTTPException(404, "Character not found")

    crud.create_turn(db, session_id=session_id, speaker="user", text=body.text)

    history = session_utils.build_history(db, session_id)

    result = await llm.generate_turn(
        character_prompt=char.character_prompt,
        history=history,
        user_text=body.text,
    )

    reply = result.get("reply", "")
    facial = result.get("facial_expression", {"label": "neutral"})
    head = result.get("head_movement", {"label": "still"})
    actions = result.get("actions", [])

    crud.create_turn(db, session_id=session_id, speaker="character", text=reply)

    return schemas.CharacterTurnOut(
        text=reply,
        facial_expression=facial,
        head_movement=head,
        actions=actions,
    )
