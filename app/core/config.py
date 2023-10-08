from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    MONGODB_URI: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int # number in minutes
    ACCESS_TOKEN_EXPIRES_IN: int # number in minutes
    JWT_ALGORITHM: str
    # Add other configuration settings as needed

    class Config:
        env_file = ".env"  # Specify the path to your .env file


settings = Settings()
