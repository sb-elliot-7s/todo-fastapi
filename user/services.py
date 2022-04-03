from fastapi import HTTPException, status
from .repositories import UserRepositoryInterface
from .password_utils import PasswordUtilsInterface
from .token_utils import TokenUtilsInterface


class UserService:
    def __init__(self, repository: UserRepositoryInterface, password_utils: PasswordUtilsInterface):
        self._repo = repository
        self._password_utils = password_utils

    async def _authenticate_user(self, username: str, password: str):
        if any([not (user := await self._repo.get_user_by_username(username=username)),
                not await self._password_utils.verify_password(plain_password=password, hashed_password=user.password)]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')
        return user

    async def login(self, username: str, password: str, jwt_utils: TokenUtilsInterface):
        user = await self._authenticate_user(username=username, password=password)
        access_token: str = await jwt_utils.create_access_token(data={'sub': user.username})
        return {'access_token': access_token, 'token_type': 'bearer'}

    async def signup(self, username: str, password: str):
        if await self._repo.get_user_by_username(username=username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this username exists')
        hashed_password = await self._password_utils.get_hashed_password(password=password)
        return await self._repo.save_user(username=username, password=hashed_password)
