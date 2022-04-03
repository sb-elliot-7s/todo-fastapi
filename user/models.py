from database.db import Base

import sqlalchemy as sa
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String(length=50), nullable=False)
    password = sa.Column(sa.String, nullable=False)

    todos = relationship('Todo', backref='user', lazy='joined', cascade='all, delete, delete-orphan', passive_deletes=False)

    def __repr__(self) -> str:
        return f'User: {self.username}'
