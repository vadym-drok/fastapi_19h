from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user_name: str
    db_user_password: str
    db_name: str
    db_host: str
    # db_port: int
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    pgadmin_email: EmailStr
    pgadmin_password: str

    class Config:
        env_file = '.env'


settings = Settings()
