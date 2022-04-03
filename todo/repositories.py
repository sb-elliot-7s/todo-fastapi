import uuid
from abc import ABC, abstractmethod
from typing import Optional
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload
from user.models import User
from .models import Todo, Image, Link
from image_utils.image_service import ImageServiceInterface


class TodoRepositoryInterface(ABC):
    @abstractmethod
    async def get_all_todos(self, user: User, limit: Optional[int], offset: Optional[int]) -> list[Todo]: pass

    @abstractmethod
    async def get_todo(self, user: User, todo_id: int) -> Todo: pass

    @abstractmethod
    async def create_todo(self, user: User, todo_data: dict, links: Optional[list[str]],
                          images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str): pass

    @abstractmethod
    async def update_todo(self, todo_id: int, user: User, updated_data: dict, links: Optional[list[str]],
                          images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str): pass

    @abstractmethod
    async def delete_todo(self, todo_id: int, user: User, image_service: ImageServiceInterface): pass


class TodoRepository(TodoRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _save_images(self, todo_id: int, images: Optional[list[UploadFile]], image_service: ImageServiceInterface,
                           host: str):
        if images:
            for image in images:
                image_name = f'{uuid.uuid4()}-&{image.filename}'
                await image_service.write_image(image_name=image_name, image=image)
                await self._session.execute(insert(Image).values(todo_id=todo_id, photo_url=f'{host}/{image_name}'))

    async def _save_links(self, todo_id: int, links: Optional[list[str]]):
        if links:
            await self._session.execute(insert(Link).values([{'todo_id': todo_id, 'url': link} for link in links]))

    async def get_all_todos(self, user: User, limit: Optional[int], offset: Optional[int]) -> list[Todo]:
        result: AsyncResult = await self._session.execute(select(Todo)
                                                          .where(Todo.user_id == user.id)
                                                          .limit(limit)
                                                          .offset(offset))
        return result.scalars().unique().all()

    async def get_todo(self, user: User, todo_id: int) -> Todo:
        result: AsyncResult = await self._session.execute(select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id))
        if not (todo := result.scalars().first()):
            raise HTTPException(detail='Todo not found', status_code=status.HTTP_404_NOT_FOUND)
        return todo

    async def create_todo(self, user: User, todo_data: dict, links: Optional[list[str]],
                          images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str):
        result: AsyncResult = await self._session.execute(insert(Todo)
                                                          .values(**todo_data, user_id=user.id)
                                                          .returning(Todo.id))
        _todo_id = result.scalars().first()
        await self._save_links(todo_id=_todo_id, links=links)
        await self._save_images(todo_id=_todo_id, images=images, image_service=image_service, host=host)
        await self._session.commit()
        # select refresh todo
        return _todo_id

    async def update_todo(self, todo_id: int, user: User, updated_data: dict, links: Optional[list[str]],
                          images: Optional[list[UploadFile]], image_service: ImageServiceInterface, host: str):
        if (todo := await self.get_todo(todo_id=todo_id, user=user)) and (todo.user_id != user.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You cannot update this todo')
        await self._save_images(todo_id=todo.id, images=images, image_service=image_service, host=host)
        await self._save_links(todo_id=todo.id, links=links)
        _: AsyncResult = await self._session.execute(update(Todo).where(Todo.id == todo_id).values(**updated_data))
        await self._session.commit()
        await self._session.refresh(todo)
        return todo

    async def delete_todo(self, todo_id: int, user: User, image_service: ImageServiceInterface):
        todo = await self.get_todo(user=user, todo_id=todo_id)
        if todo.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You cannot delete this todo')
        images = todo.images
        if images:
            for image in images:
                await image_service.delete_image(image_name=image.photo_url.split('/')[-1])
        await self._session.delete(todo)
        await self._session.commit()
