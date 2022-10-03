from datetime import datetime, timedelta

from fastapi import status
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from msscore import models, schemas
from msscore.auth import pwd_context, SECRET_KEY, ALGORITHM
from msscore.database import SessionLocal
from msscore.schemas import TokenData
from fastapi import Depends
from msscore.auth import oauth2_scheme


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_score(db: Session, user_name: str):
    return db.query(models.Score).filter(models.Score.user_name == user_name).all()


def create_score(db: Session, score: schemas.Score):
    score_data = models.Score(**score.dict())
    db.add(score_data)
    db.commit()
    db.refresh(score_data)
    return score_data


if __name__ == '__main__':
    hashed_password = get_password_hash("king")
    print(hashed_password)
