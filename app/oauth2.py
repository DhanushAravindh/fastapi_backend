from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret_key
# Algorithm
# Validity

secret_key = settings.SECRET_KEY
algo = settings.ALGORITHM
access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRES_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algo)
    return encoded_jwt


def verify_access_token(token: str, details_exception):
    try:
        val = jwt.decode(token, secret_key, [algo])
        id: str = val.get("user_id")
        if id is None:
            raise details_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise details_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    details_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="couln't find teh details entered", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, details_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    print(user.__dict__)
    return user
