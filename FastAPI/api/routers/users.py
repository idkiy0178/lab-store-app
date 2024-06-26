from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserCreate, User
from sqlalchemy.orm.session import Session

from services.user import get_current_active_user
from api.deps import get_db
from crud import user as user_crud


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return user_crud.create(db=db, user=user)