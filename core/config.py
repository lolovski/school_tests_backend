from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    api_token: str
    admin_id: str
    secret_jwt: str
    secret_admin_jwt: str
    secret_user: str
    server_id: str
    ip_address: str
    first_class_name: Optional[str]

    first_superadmin_email: Optional[EmailStr]
    first_superadmin_password: Optional[str]
    first_superadmin_last_name: Optional[str]
    first_superadmin_first_name: Optional[str]
    first_superadmin_middle_name: Optional[str]

    first_user_email: Optional[str]
    first_user_password: Optional[str]
    first_user_last_name: Optional[str]
    first_user_first_name: Optional[str]
    first_user_middle_name: Optional[str]
    first_user_class_id: Optional[str]

    first_teacher_email: Optional[str]
    first_teacher_password: Optional[str]
    first_teacher_last_name: Optional[str]
    first_teacher_first_name: Optional[str]
    first_teacher_middle_name: Optional[str]
    first_teacher_class_id: Optional[str]



    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()