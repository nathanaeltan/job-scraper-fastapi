from src.auth.models import Users
from src.auth.utils import bcrypt_context
from src.database import db_dependency


def create_db_user(db: db_dependency, user_to_create: Users):
    db.add(user_to_create)
    db.commit()


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user
