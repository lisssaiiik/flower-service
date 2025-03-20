from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    
    QUEUE_NAME: str
    DONE_QUEUE_NAME: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    class Config:
        env_file = "rabbit/.env"


settings = Settings()