from typing import Optional
from fastapi import APIRouter, status, Depends, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from user.models import User
from .services import TodoService
from .repositories import TodoRepository
from permissions.user_permissions import UserPermissions
from user.token_utils import TokenUtils
from configs import get_settings, IMAGES_DIR
from .schemas import CreateTodoSchema, TodoSchema
from image_utils.image_service import ImageService

todo_router = APIRouter(prefix='/todos', tags=['todos'])
user_permissions = UserPermissions(
    token_service=TokenUtils(secret_key=get_settings().secret_key, algorithm=get_settings().algorithm,
                             exp_time=get_settings().access_token_expire_minutes))


@todo_router.get('/', status_code=status.HTTP_200_OK, response_model=list[TodoSchema])
async def get_all_todos(limit: int = 20, offset: int = 0, user: User = Depends(user_permissions),
                        session: AsyncSession = Depends(get_db)):
    return await TodoService(repository=TodoRepository(session=session)).get_all_todos(limit=limit, offset=offset, user=user)


@todo_router.get('/{todo_id}', status_code=status.HTTP_200_OK, response_model=TodoSchema)
async def get_todo(todo_id: int, user: User = Depends(user_permissions), session: AsyncSession = Depends(get_db)):
    return await TodoService(repository=TodoRepository(session=session)).get_todo(todo_id=todo_id, user=user)


@todo_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(session: AsyncSession = Depends(get_db),
                      todo_data: CreateTodoSchema = Depends(CreateTodoSchema.as_form),
                      links: Optional[list[str]] = Form(None),
                      images: Optional[list[UploadFile]] = File(None),
                      user: User = Depends(user_permissions)):
    return await TodoService(repository=TodoRepository(session=session)) \
        .create_todo(user=user, todo_data=todo_data, images=images, links_data=links, host=get_settings().image_host,
                     image_service=ImageService(path=IMAGES_DIR))


@todo_router.put('/{todo_id}', status_code=status.HTTP_200_OK, response_model=TodoSchema)
async def update_todo(todo_id: int, session: AsyncSession = Depends(get_db),
                      updated_data: CreateTodoSchema = Depends(CreateTodoSchema.as_form),
                      images: Optional[list[UploadFile]] = File(None),
                      links: Optional[list[str]] = Form(None),
                      user: User = Depends(user_permissions)):
    return await TodoService(repository=TodoRepository(session=session)) \
        .update_todo(todo_id=todo_id, updated_data=updated_data, user=user, image_service=ImageService(path=IMAGES_DIR),
                     host=get_settings().image_host, links_data=links, images=images)


@todo_router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, session: AsyncSession = Depends(get_db), user: User = Depends(user_permissions)):
    return await TodoService(repository=TodoRepository(session=session)) \
        .delete_todo(todo_id=todo_id, user=user, image_service=ImageService(path=IMAGES_DIR))
