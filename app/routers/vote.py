from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(
    payload: schemas.VoteCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Post does not exits",
                "data": {
                    "post_id": payload.post_id,
                },
            },
        )
    query = db.query(models.Vote).filter(
        models.Vote.post_id == payload.post_id,
        models.Vote.user_id == current_user.id,
    )
    vote = query.first()
    if payload.dir == 1:
        try:
            if vote:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "message": "Duplicate Vote",
                        "data": {
                            "post_id": payload.post_id,
                            "user_id": current_user.id,
                        },
                    },
                )
            else:
                new_vote = models.Vote(post_id=payload.post_id, user_id=current_user.id)
                db.add(new_vote)
                db.commit()
                db.refresh(new_vote)
                return {"message": "Vote added successfully"}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Duplicate vote",
                    "data": {"post_id": payload.post_id, "user_id": current_user.id},
                },
            )
    else:
        if vote:
            query.delete()
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Vote does not exist",
                    "data": {"post_id": payload.post_id, "user_id": current_user.id},
                },
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
