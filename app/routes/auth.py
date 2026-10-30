from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Player
from app.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.security import create_access_token, hash_password, verify_password
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.scalar(
        select(Player).where(or_(Player.username == payload.username, Player.email == payload.email))
    )
    if existing:
        raise HTTPException(status_code=409, detail="Username or email is already registered.")

    player = Player(
        username=payload.username,
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
    )
    db.add(player)
    try:
        db.commit()
        db.refresh(player)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email is already registered.")

    return TokenResponse(
        access_token=create_access_token(str(player.id)),
        expires_in=settings.access_token_minutes * 60,
        player=player,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    player = db.scalar(select(Player).where(Player.email == str(payload.email).lower()))
    if player is None or not verify_password(payload.password, player.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    return TokenResponse(
        access_token=create_access_token(str(player.id)),
        expires_in=settings.access_token_minutes * 60,
        player=player,
    )
