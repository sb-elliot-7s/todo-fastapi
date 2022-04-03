from abc import ABC, abstractmethod

from passlib.context import CryptContext


class PasswordUtilsInterface(ABC):
    @abstractmethod
    async def get_hashed_password(self, password: str): pass

    @abstractmethod
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool: pass


class PasswordUtils(PasswordUtilsInterface):

    def __init__(self, password_context: CryptContext):
        self._password_context = password_context

    async def get_hashed_password(self, password: str):
        return self._password_context.hash(password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._password_context.verify(secret=plain_password, hash=hashed_password)
