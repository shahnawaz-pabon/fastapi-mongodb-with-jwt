from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    MONGODB_URI: str
    # Add other configuration settings as needed

    class Config:
        env_file = ".env"  # Specify the path to your .env file


settings = Settings()
