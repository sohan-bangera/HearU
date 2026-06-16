import random
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Audio, HeardAudio, MarkHeardRequest
from app.storage import upload_audio
from app.moderation import check_audio

router = APIRouter()

@router.post("/upload")
async def upload_audio_route(
    audio: UploadFile = File(...),
    category: str = Form(...),
    session_token: str = Form(...),
    db: Session = Depends(get_session)
):
    audio_bytes = await audio.read()
    filename = f"{uuid.uuid4()}.webm"
    audio_url = upload_audio(audio_bytes, filename)
    new_audio = Audio(
        category=category,
        audio_url=audio_url,
        duration=0,
        is_approved=False
    )
    db.add(new_audio)
    db.commit()
    db.refresh(new_audio)

    is_appropriate = await check_audio(audio_url)

    if is_appropriate:
        new_audio.is_approved = True
        db.add(new_audio)
        db.commit()
        return {"status": "approved", "message": "Your voice has been heard!"}
    else:
        new_audio.is_flagged = True
        db.add(new_audio)
        db.commit()
        return {"status": "flagged", "message": "This audio contains inappropriate content."}
    
@router.get("/random")
def get_random_audio(
    category: str,
    session_token: str,
    db: Session = Depends(get_session)
):
    heard_ids = db.exec(
        select(HeardAudio.audio_id).where(HeardAudio.session_token == session_token)
    ).all()

    query = select(Audio).where(
        Audio.category == category,
        Audio.is_approved == True,
        Audio.id.notin_(heard_ids)
    )
    audios = db.exec(query).all()

    if not audios:
        raise HTTPException(status_code=404, detail="No more audio available")
    
    chosen = random.choice(audios)

    return {
        "audio_id": chosen.id,
        "audio_url": chosen.audio_url,
        "category": chosen.category,
        "duration": chosen.duration
    }

@router.post("/mark-heard")
def mark_heard(
    payload: MarkHeardRequest,
    db: Session = Depends(get_session)
):
    heard = HeardAudio(
        session_token=payload.session_token,
        audio_id=payload.audio_id
    )
    db.add(heard)
    db.commit()
    return {"success": True}