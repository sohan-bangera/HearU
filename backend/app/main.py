from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.routes import audio, stats

app = FastAPI(title="HearU API")

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], #React Dev Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

