from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import Task, TaskImage, TaskCategory, ImageCategory, DifficultyLevel
from requests.base import RequestsBase


class TaskRequests(RequestsBase):
    ...


task_requests = TaskRequests(Task)


class TaskImageRequests(RequestsBase):
    ...


task_image_requests = TaskImageRequests(TaskImage)


class TaskCategoryRequests(RequestsBase):
    ...


task_category_requests = TaskCategoryRequests(TaskCategory)


class ImageCategoryRequests(RequestsBase):
    ...


image_category_requests = ImageCategoryRequests(ImageCategory)


class DifficultyLevelRequests(RequestsBase):
    ...


difficulty_level_requests = DifficultyLevelRequests(DifficultyLevel)