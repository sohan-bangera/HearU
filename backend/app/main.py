from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routes import audio, stats

# lifespan handles the startup and shutdown events
# Everything before yield runs when server starts
# Everything after yield runs when server shuts down
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables() # create DB tables on startup
    yield                  # Server is now running and accepting requests

app = FastAPI(title="HearU API", lifespan=lifespan)

# Allow React frontend to talk to this backend
# Withour this, browser blocks all requests from localhost:5173 to localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React Dev Server
    allow_credentials=True,                  # Allow session tokens/cookies  
    allow_methods=["*"],                     # Allow GET, POST, PUT, DELETE etc 
    allow_headers=["*"],                     # Allow all request headers
)

app.include_router(audio.router, prefix="/audio", tags=["audio"])
app.include_router(stats.router, tags=["stats"])

@app.get("/")
def root():
    return {"message":"HearU API is running"}