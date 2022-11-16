from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from .. import database
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
def login(user_values: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_values.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the user with the entered email not found")
    if not utils.verify(user_values.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user with the entered email not found")

    # create a token
    # return token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}
