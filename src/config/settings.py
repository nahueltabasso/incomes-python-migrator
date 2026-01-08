from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
    
    API_URL: str
    USERNAMES: str
    PASSWORD: str
    COMMON_PASSWORD: str
    
    
settings = Settings()  # type: ignore