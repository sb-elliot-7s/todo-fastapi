from typing import Optional

from fastapi import UploadFile

from image_utils.image_service import ImageServiceInterface
from user.models import User
from .repositories import TodoRepositoryInterface
from .schemas import CreateTodoSchema


class TodoService:
    def __init__(self, repository: TodoRepositoryInterface):
        self._repository = repository

    async def get_all_todos(self, limit: int, offset: int, user: User):
        return await self._repository.get_all_todos(limit=limit, offset=offset, user=user)

    async def get_todo(self, todo_id: int, user: User):
        return await self._repository.get_todo(todo_id=todo_id, user=user)

    async def create_todo(self, user: User, todo_data: CreateTodoSchema, links_data: Optional[list[str]],
                          images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str):
        return await self._repository.create_todo(user=user, todo_data=todo_data.dict(exclude_none=True),
                                                  links=links_data, images=images, image_service=image_service, host=host)

    async def update_todo(self, todo_id: int, user: User, updated_data: CreateTodoSchema, links_data: Optional[list[str]],
                          images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str):
        return await self._repository.update_todo(todo_id=todo_id, user=user, updated_data=updated_data.dict(exclude_none=True),
                                                  links=links_data, images=images, image_service=image_service, host=host)

    async def delete_todo(self, todo_id: int, user: User, image_service: ImageServiceInterface):
        return await self._repository.delete_todo(todo_id=todo_id, user=user, image_service=image_service)
