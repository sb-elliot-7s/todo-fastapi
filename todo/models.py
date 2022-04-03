from datetime import datetime

from database.db import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Todo(Base):
    __tablename__ = 'todos'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String(length=255), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'))
    description = sa.Column(sa.String, nullable=True)
    created = sa.Column(sa.DateTime, default=datetime.now)

    images = relationship('Image', backref='todo', lazy='joined', cascade="all, delete, delete-orphan", passive_deletes=False)
    links = relationship('Link', backref='todo', lazy='joined', cascade="all, delete, delete-orphan", passive_deletes=False)

    def __repr__(self) -> str:
        return f'{self.title}'


class Link(Base):
    __tablename__ = 'links'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    todo_id = sa.Column(sa.Integer, sa.ForeignKey('todos.id', ondelete='CASCADE'))
    url = sa.Column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.id} {self.url}'


class Image(Base):
    __tablename__ = 'images'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    todo_id = sa.Column(sa.Integer, sa.ForeignKey('todos.id', ondelete='CASCADE'))
    photo_url = sa.Column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.photo_url}'
