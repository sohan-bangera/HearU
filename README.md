# HearU 🎙️

### Anonymous Audio Recording & Listening Platform

HearU is a full-stack platform where users can anonymously record
and share voice messages by category, and listen to others —
without any account or login required.

## Tech Stack

- **Backend:** FastAPI + SQLModel + PostgreSQL (Supabase)
- **Frontend:** Reflex (Python → React)
- **Storage:** Supabase Storage
- **AI Moderation:** AssemblyAI

## Features

- 🎙 Record anonymous voice messages by category
- 🎧 Listen to random voices — no repeats
- 🤖 AI content moderation via AssemblyAI
- 🔒 Fully anonymous — no login required

## Status

🚧 In progress

## Setup

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# Frontend
cd frontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
reflex run
```
