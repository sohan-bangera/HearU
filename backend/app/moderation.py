import asyncio
import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_KEY")

async def check_audio(audio_url: str) -> bool:
    try:
        transcript = await asyncio.to_thread(
            _transcribe_audio, audio_url
        )

        if transcript.content_safety_labels:
            for result in transcript.content_safety_labels.results:
                for label in result.labels:
                    if label.confidence > 0.7:
                        return False
        
        return True
    
    except Exception as e:
        print(f"Moderation error: {e}")
        return True
    
def _transcribe_audio(audio_url: str):
    config = aai.TranscriptionConfig(content_safety=True)
    return aai.Transcriber().transcribe(audio_url, config)