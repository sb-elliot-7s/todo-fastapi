from abc import ABC, abstractmethod
from fastapi import UploadFile
import aiofiles
from aiofiles import os as _os


class ImageServiceInterface(ABC):
    @abstractmethod
    async def read_image(self, image_name: str): pass

    @abstractmethod
    async def write_image(self, image_name: str, image: UploadFile): pass

    @abstractmethod
    async def delete_image(self, image_name: str): pass


class ImageService(ImageServiceInterface):

    def __init__(self, path: str):
        self._path = path

    async def read_image(self, image_name: str):
        try:
            async with aiofiles.open(f'{self._path}/{image_name}', mode='r') as f:
                image = await f.read()
            return image
        except FileNotFoundError as e:
            raise FileNotFoundError(e)

    async def write_image(self, image_name: str, image: UploadFile):
        async with aiofiles.open(f'{self._path}/{image_name}', mode='wb') as f:
            content = await image.read()
            await f.write(content)

    async def delete_image(self, image_name: str):
        try:
            await _os.remove(f'{self._path}/{image_name}')
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
