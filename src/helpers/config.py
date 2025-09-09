from pydantic_settings import BaseSettings, SettingsConfigDict
 
class Settings(BaseSettings):

    APP_Name: str
    APP_Version: str
    APP_Description: str
    APP_Author: str
    File_allowed_extensions: list
    File_max_size: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGODB_DATABASE_url:str
    MONGODB_DATABASE:str

    class Config:
         env_file = ".env"
    
def get_settings():
    return Settings()   