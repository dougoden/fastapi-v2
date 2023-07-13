from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import hash_pwd

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id).all()
    return users


@router.get("/{id}", response_model=schemas.User)
def get_post(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"User with id: {id} was not found"},
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    payload.password = hash_pwd(payload.password)
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"User with id: {id} was not found"},
        )
    query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def update_User(id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    payload.updated_at = datetime.now()
    payload.password = hash_pwd(payload.password)
    query = db.query(models.User).filter(models.User.id == id)
    post = query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"User with id: {id} was not found"},
        )
    query.update(payload.dict())
    db.commit()
    return query.first()
