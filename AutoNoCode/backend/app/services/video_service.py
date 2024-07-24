from app.models import Video
from sqlalchemy.orm import Session


def get_videos(db: Session):
    return db.query(Video).all()


def create_video(db: Session, video_data):
    new_video = Video(**video_data)
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video
