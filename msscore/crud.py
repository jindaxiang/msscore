from sqlalchemy.orm import Session

from msscore import models, schemas


def get_user(db: Session, user_name: str):
    return db.query(models.Score).filter(models.Score.user_name == user_name).all()


def create_user(db: Session, score: schemas.Score):
    score_data = models.Score(**score.dict())
    print('888888888888', score_data.user_name)
    db.add(score_data)
    db.commit()
    db.refresh(score_data)
    return score_data

