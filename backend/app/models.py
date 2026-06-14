from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid

class Audio(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    category: str
    audio_url: str
    duration: float
    is_approved: bool = Field(default=False)
    is_flagged: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HeardAudio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_token: str
    audio_id: str
    heard_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MarkHeardRequest(SQLModel):
    audio_id: str
    session_token: str