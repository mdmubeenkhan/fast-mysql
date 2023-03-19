from pydantic import BaseSettings

# Best practice to declare environment variable is in UPPER CASE but not mandatory
# pytdantic treats environment variable in in-sensitive way
# pydantic automatically converts the env variable type to required variable type
class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT:str
    DATABASE_NAME:str
    DATABASE_USERNAME:str
    DATABASE_PASSWORD:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MIN:int

    class Config:
        env_file = ".env"
settings = Settings()