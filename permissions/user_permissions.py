from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from database.db import get_db
from user.models import User

from user.token_utils import TokenUtilsInterface


class UserPermissions:
    OAUTH_TOKEN = OAuth2PasswordBearer(tokenUrl='/users/login')

    def __init__(self, token_service: TokenUtilsInterface):
        self._token_service = token_service

    async def __call__(self, token: str = Depends(OAUTH_TOKEN), session: AsyncSession = Depends(get_db)):
        payload = await self._token_service.decode_access_token(token=token)
        result: AsyncResult = await session.execute(select(User).where(User.username == payload.get('sub')))
        if not (user := result.scalars().first()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
        return user
