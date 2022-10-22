import os
from logging import config as logging_config
from typing import Union

from pydantic import BaseSettings, EmailStr

from src.core.logger import LOGGING


class Settings(BaseSettings):
    app_title: str = 'Сервис для создания коротких ссылок'
    description: str = 'Сделай ссылку которой легко поделиться с друзьями!'
    secret: str = os.getenv('SECRET',
                            default='iuahgbhiulcb15674dzxcvcnds')
    database_url: str = os.getenv('DATABASE_URL',
                                  default='sqlite+aiosqlite:///./fastapi.db')
    project_host: str = os.getenv('PROJECT_HOST', default='127.0.0.1')
    project_port: str = os.getenv('PROJECT_PORT', default='8000')
    first_superuser_email: Union[None, EmailStr] = None
    first_superuser_password: Union[None, str] = None

    class Config:
        env_file = '.env'


settings = Settings()

logging_config.dictConfig(LOGGING)
