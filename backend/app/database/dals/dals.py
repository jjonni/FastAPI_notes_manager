# Здесь будет data access control layer

from sqlalchemy.orm import Session

from backend.app.database.models.models import *

class UserDAL:
    def __init__(self, session: Session):
        self.db_session = session

    ...

class NoteDAL:
    def __init__(self, session: Session):
        self.db_session = session

    ...

class TagDAL:
    def __init__(self, session: Session):
        self.db_session = session

    ...

class NoteTagDAL:
    def __init__(self, session: Session):
        self.db_session = session

    ...