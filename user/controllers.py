from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from .schemas import CreateUserSchema, JWTTokenSchema
from .services import UserService
from .repositories import UserRepository
from .password_utils import PasswordUtils
from .token_utils import TokenUtils
from configs import get_settings

user_router = APIRouter(prefix='/users', tags=['users'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@user_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user_data: CreateUserSchema, session: AsyncSession = Depends(get_db)):
    return await UserService(repository=UserRepository(session=session), password_utils=PasswordUtils(password_context=pwd_context)) \
        .signup(username=user_data.username, password=user_data.password)


@user_router.post('/login', response_model=JWTTokenSchema, status_code=status.HTTP_200_OK)
async def login(user_form: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    return await UserService(repository=UserRepository(session=session), password_utils=PasswordUtils(password_context=pwd_context)) \
        .login(username=user_form.username, password=user_form.password,
               jwt_utils=TokenUtils(secret_key=get_settings().secret_key, algorithm=get_settings().algorithm,
                                    exp_time=get_settings().access_token_expire_minutes))
