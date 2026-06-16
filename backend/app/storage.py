import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def upload_audio(file_bytes, filename: str) -> str:
    bucket = "audio"

    supabase.storage.from_(bucket).upload(
        path=filename,
        file=file_bytes,
        file_options={"content-type": "audio/webm"}
    )

    public_url = supabase.storage.from_(bucket).get_public_url(filename)
    return public_url

