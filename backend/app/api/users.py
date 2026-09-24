from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    user = User(
        email=user_data.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user