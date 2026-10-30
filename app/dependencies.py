import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Player
from app.security import decode_access_token

bearer_scheme = HTTPBearer()


def get_current_player(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Player:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(credentials.credentials)
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
