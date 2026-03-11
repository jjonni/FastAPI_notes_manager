# Здесь будет data access control layer
# Но без классов, чисто на функциях
# Возможно впоследствии разобью на несколько файлов, каждый из которых будет относиться к соответствующей ORM модели

from sqlalchemy.orm import Session

from backend.app.database.models.models import *

def create_user(session: Session, name: str, surname: str, email: str, password_hash: str) -> User:
    new_user = User(name=name, surname=surname, email=email, password_hash=password_hash)
    session.add(new_user)
    session.flush()
    return new_user