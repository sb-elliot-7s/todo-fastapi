from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from .models import User
from database.db import get_db


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def save_user(self, username: str, password: str): pass

    @abstractmethod
    async def get_user_by_username(self, username: str): pass


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_user(self, username: str, password: str):
        result = await self._session.execute(insert(User).values(username=username, password=password).returning(User.id))
        await self._session.commit()
        return result.first()

    async def get_user_by_username(self, username: str):
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalars().first()
