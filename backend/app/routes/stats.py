from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Audio

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_session)):
    audios = db.exec(
        select(Audio).where(Audio.is_approved == True)
    ).all()
    return {"total_voices": len(audios)}