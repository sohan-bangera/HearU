import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

async def get_stats() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/stats")
        return response.json()
    
async def get_random_audio(category: str, session_token: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/audio/random",
            params={"category": category, "session_token": session_token}
        )
        if response.status_code == 404:
            return None
        return response.json()
    

async def mark_heard(audio_id: str, session_token: str) -> dict:
    async with httpx.AsynClient() as client:
        response = await client.post(
            f"{API_URL}/audio/mark-heard",
            json={"audio_id": audio_id, "session_token": session_token}
        )
        return response.json()
    
async def upload_audio(audio_bytes: bytes, category: str, session_token: str) -> dict:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{API_URL}/audio/upload",
            files={"audio":("recording.webm", audio_bytes, "audio/webm")},
            data={"category":category, "session_token":session_token}
        )
        return response.json()