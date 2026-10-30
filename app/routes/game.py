from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_player
from app.game_data import MISSIONS, WORK_TASKS
from app.models import Player, PlayerActivity
from app.schemas import GameActionResponse, PlayerResponse

router = APIRouter(prefix="/api/game", tags=["game progression"])


def _award(player: Player, reward: dict) -> None:
    player.credits += reward["credits"]
    player.reputation = min(100, player.reputation + reward["reputation"])
    player.energy = max(0, player.energy - reward["energy"])
    player.focus = max(0, player.focus - reward["focus"])
    player.experience += reward["experience"]
    while player.experience >= 100:
        player.experience -= 100
        player.level += 1


@router.post("/work/{task_id}", response_model=GameActionResponse)
def complete_work(task_id: str, player: Player = Depends(get_current_player), db: Session = Depends(get_db)):
    task = WORK_TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="That work task does not exist.")
    if player.energy < task["energy"] or player.focus < task["focus"]:
        raise HTTPException(status_code=409, detail="Not enough energy or focus for this task.")

    now = datetime.now(timezone.utc)
    daily_key = f"{task_id}:{now.date().isoformat()}"
    activity = PlayerActivity(player_id=player.id, activity_type="work", activity_key=daily_key, completed_at=now)
    db.add(activity)
    try:
        _award(player, task)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="You have already completed this work task today.")
    db.refresh(player)
    return GameActionResponse(message=f"Completed: {task['title']}. Rewards saved to your account.", player=PlayerResponse.model_validate(player))


@router.post("/missions/{mission_id}", response_model=GameActionResponse)
def complete_mission(mission_id: str, player: Player = Depends(get_current_player), db: Session = Depends(get_db)):
    mission = MISSIONS.get(mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="That community mission does not exist.")
    already_done = db.scalar(select(PlayerActivity.id).where(
        PlayerActivity.player_id == player.id,
        PlayerActivity.activity_type == "mission",
        PlayerActivity.activity_key == mission_id,
    ))
    if already_done:
        raise HTTPException(status_code=409, detail="You have already completed this mission.")
    if player.energy < mission["energy"] or player.focus < mission["focus"]:
        raise HTTPException(status_code=409, detail="Not enough energy or focus for this mission.")

    db.add(PlayerActivity(player_id=player.id, activity_type="mission", activity_key=mission_id))
    try:
        _award(player, mission)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="This mission was already completed.")
    db.refresh(player)
    return GameActionResponse(message=f"Mission complete: {mission['title']}. Rewards saved to your account.", player=PlayerResponse.model_validate(player))

@router.get("/status")
def get_game_status(player: Player = Depends(get_current_player), db: Session = Depends(get_db)):
    today = datetime.now(timezone.utc).date().isoformat()
    activities = db.scalars(select(PlayerActivity).where(PlayerActivity.player_id == player.id)).all()
    completed_missions = [item.activity_key for item in activities if item.activity_type == "mission"]
    completed_work = [item.activity_key.split(":", 1)[0] for item in activities
                      if item.activity_type == "work" and item.activity_key.endswith(":" + today)]
    return {"completed_missions": completed_missions, "completed_work_today": completed_work}
