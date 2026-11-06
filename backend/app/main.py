import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import transliteration, translation, improvement, knowledge, evaluation, system
from app.services.rag_service import rag_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure directories exist
    os.makedirs("storage/faiss", exist_ok=True)
    os.makedirs("storage/documents", exist_ok=True)
    os.makedirs("storage/uploads", exist_ok=True)
    print(f"[IndicWrite AI] Initialized FastAPI backend on port {settings.BACKEND_PORT}.")
    print(f"[IndicWrite AI] FAISS vectors loaded: {rag_service.faiss_manager.count()}")
    yield
    print("[IndicWrite AI] Shutting down.")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Undergraduate CS3235 Mini-Project: Multilingual Hinglish Smart Writing Assistant based on AI4Bharat and BharatGen.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(system.router)
app.include_router(transliteration.router)
app.include_router(translation.router)
app.include_router(improvement.router)
app.include_router(knowledge.router)
app.include_router(evaluation.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.BACKEND_PORT, reload=True)
