from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]

)


@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), user_id=Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip)

    return post.all()


# a title is mandatory and some content

# Create a session for every request toward that specific api endpoint


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # To prevent sql commends being passed as input %s is used to ensure proper input is being passed

    # cursor.execute("""INSERT INTO posts (title,content,is_published) VALUES (%s,%s,%s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    print(post.dict())
    new_post = models.Post(user_id=current_user.id, **post.dict())
    # manually assigning values is inefficent if no of columns increases
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# path parameter

# convert id into int and validate and convert id back to a string
@router.get('/{id}', response_model=schemas.PostVote)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts where id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"meassage for post-{id} not found")
    return post

# pass input via a placeholder %s


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def Delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def Update_post(id: int, val: schemas.CreatePost, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s ,content=%s,is_published= %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query.update(val.dict(), synchronize_session=False)
    db.commit()

    return post
