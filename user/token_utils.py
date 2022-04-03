from abc import ABC, abstractmethod
from typing import Optional

from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta


class TokenUtilsInterface(ABC):
    @abstractmethod
    async def create_access_token(self, data: dict): pass

    @abstractmethod
    async def decode_access_token(self, token: str): pass


class TokenUtils(TokenUtilsInterface):

    def __init__(self, secret_key: str, algorithm: Optional[str], exp_time: Optional[int] = None):
        self._secret_key = secret_key
        self._exp_time = exp_time
        self._algorithm = algorithm

    async def create_access_token(self, data: dict):
        data = data.copy()
        exp_time = datetime.utcnow() + timedelta(minutes=self._exp_time) if self._exp_time else datetime.utcnow() + timedelta(minutes=30)
        data.update({'exp': exp_time})
        return jwt.encode(data, key=self._secret_key, algorithm=self._algorithm)

    async def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(token, key=self._secret_key, algorithms=self._algorithm)
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='not validate credentials', headers={"WWW-Authenticate": "Bearer"})
        return payload
