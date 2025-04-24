from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models import User
from app.schemas.user import UserDTO
from app.auth import pwd_context

router = APIRouter()


@router.post("/user/register")
async def register_user(user_data: UserDTO, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with specified username already exists"
        )

    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(username=user_data.username, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": f"User {new_user.username} created successfully",
        "user_id": new_user.id,
    }
