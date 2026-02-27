from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import PasswordChange, UserUpdate


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    if data.name is not None:
        user.name = data.name
    if data.email is not None:
        user.email = data.email
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user: User, data: PasswordChange) -> bool:
    if not user.hashed_password or not verify_password(data.current_password, user.hashed_password):
        return False
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    return True
