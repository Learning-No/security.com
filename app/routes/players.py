from fastapi import APIRouter, Depends
from app.dependencies import get_current_player
from app.models import Player
from app.schemas import PlayerResponse

router = APIRouter(prefix="/api/players", tags=["players"])


@router.get("/me", response_model=PlayerResponse)
def get_my_profile(player: Player = Depends(get_current_player)):
    return player
