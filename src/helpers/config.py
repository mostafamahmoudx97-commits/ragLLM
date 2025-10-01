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


    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str = None
    OPENAI_API_URL:str=None

    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None
    INPUT_DAFAULT_MAX_CHARACTERS: int = None
    GENERATION_DAFAULT_MAX_TOKENS: int = None
    GENERATION_DAFAULT_TEMPERATURE: float = None

    VECTOR_DB_BACKEND:str
    VECTOR_DB_PATH:str
    VECTOR_DB_DISTANCE_METHOD:str =None
    PRIMARY_LANG: str = "en"
    DEFAULT_LANG: str = "en"

    class Config:
         env_file = ".env"
    
def get_settings():
    return Settings()   