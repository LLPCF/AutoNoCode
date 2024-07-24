from app.database import get_db
from app.services.video_service import create_video, get_videos
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def read_videos(db: Session = Depends(get_db)):
    return get_videos(db)


@router.post("/")
async def add_video(video_data: dict, db: Session = Depends(get_db)):
    return create_video(db, video_data)
