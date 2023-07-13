from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_name: str
    db_port: str
    db_pwd: str
    db_url: str
    db_user: str

    access_token_expire_minutes: int
    algorithm: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
