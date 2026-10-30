from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import settings
from app.database import Base, engine
from app import models  # noqa: F401 - registers SQLAlchemy models
from app.routes import auth, players


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Convenient for the starter build. Use Alembic migrations before production.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Ironhaven multiplayer RPG API foundation.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(players.router)


@app.get("/api/health", tags=["system"])
def health():
    return {"status": "ok", "service": "ironhaven-api", "version": "0.1.0"}


@app.get("/", include_in_schema=False)
def homepage():
    """Serve the browser client from the same origin as the API."""
    index_file = Path(__file__).resolve().parent.parent / "index.html"
    return FileResponse(index_file)
