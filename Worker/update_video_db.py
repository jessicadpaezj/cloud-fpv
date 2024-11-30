from model import db_session, Video


def update_video_status(video_id, status):
     video = db_session.query(Video).filter(Video.id == int(video_id)).first()
     if video:
        video.status = status
        db_session.commit()
     else:
        print("No such video exists")