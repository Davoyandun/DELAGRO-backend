# import os
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     API_V1_STR: str = "/api/v1"
#     PROJECT_NAME: str = "DelAgro"
#     PROJECT_VERSION: str = "0.1.0"
#     SQLALCHEMY_DATABASE_URI: str = "mysql+mysqlconnector://delAgroAdmin:delAgroPassword@delagroidenfitier.c9om0o8ocr45.us-east-1.rds.amazonaws.com:3306/delAgroDB"

# settings = Settings()

# todo esto debe venir de variables de entorno


import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "DelAgro")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
