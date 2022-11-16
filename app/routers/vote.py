from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id) 
    vote_post = db_query.first()
    if vote.dir ==1:
        if vote_post:
            return HTTPException(status_code=status.HTTP_409_CONFLICT)
        new_vote = models.Vote(post_id = vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
    else:
        if not vote_post:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        db_query.delete(synchronize_session=False)
        db.commit()
    return {"success"}

    
