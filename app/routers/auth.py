from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db
from ..utils import verify_pwd
from ..schemas import Token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == payload.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": f"Invalid credintials"},
        )
    if not verify_pwd(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": f"Invalid credintials"},
        )
    access_token = oauth2.create_access_token(payload={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
