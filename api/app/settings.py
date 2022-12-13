import os
from typing import Optional, List

from pydantic import BaseSettings


class Settings(BaseSettings):
    ISSUER: Optional[str] = os.getenv('ISSUER')
    DEBUG: bool = os.getenv('DEBUG') == 'true'

    class JWT:
        SECRET: Optional[str] = os.getenv('JWT_SECRET')
        ISSUER: Optional[str] = os.getenv('JWT_ISSUER')

    class DB:
        HOST: str = os.getenv('ASKLORA_HOST') if os.getenv(
            'ASKLORA_HOST') is not None else 'db'
        DB: Optional[str] = os.getenv('ASKLORA_DB') if os.getenv(
            'TEST') is None else 'asklora_test'
        USER: Optional[str] = os.getenv('ASKLORA_USER') if os.getenv(
            'TEST') is None else 'asklora_test'
        PASSWORD: Optional[str] = os.getenv('ASKLORA_PASSWORD') if os.getenv(
            'TEST') is None else 'asklora_test'

    class Middleware:
        ORIGINS: List = [
            "http://localhost:31000",
            "localhost"
        ]


settings: Settings = Settings()
