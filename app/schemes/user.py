import re
from typing import Optional

from fastapi_users import schemas
from pydantic import Field, root_validator, ConfigDict


class UserCreate(schemas.BaseUserCreate):
    email: str = Field()
    password: str = Field(min_length=8, max_length=100)
    last_name: str = Field()
    first_name: str = Field()
    middle_name: Optional[str] = Field(None)
    class_id: Optional[int] = Field(None)

    class Config:
        title = 'Создание пользователя'
        str_min_length = 2
        str_max_length = 32

    @root_validator(skip_on_failure=True)
    def using_latin(cls, values):
        if values.get('middle_name') is None:
            lfm_list = ['last_name', 'first_name']
        else:
            lfm_list = ['last_name', 'first_name', 'middle_name']
        for i in lfm_list:
            if re.search('[а-яё ]', values.get(i), re.IGNORECASE):
                continue
            else:
                raise ValueError('ФИО не может содержать латиницу и цифры')
        return values


class UserRead(schemas.BaseUser):
    id: int
    email: str
    first_name: str
    last_name: str
    middle_name: str
    class_id: Optional[int] = Field(None)
    is_superuser: bool
    status_id: Optional[int] = Field(None)

    class Config:
        model_config = ConfigDict(from_attributes=True)  #


class UserUpdate(schemas.BaseUser):
    email: str
