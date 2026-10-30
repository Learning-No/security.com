import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Player
from app.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_player(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Player:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if not subject:
            raise unauthorized
        player_id = int(subject)
    except (jwt.InvalidTokenError, TypeError, ValueError):
        raise unauthorized

    player = db.get(Player, player_id)
    if player is None:
        raise unauthorized
    return player
