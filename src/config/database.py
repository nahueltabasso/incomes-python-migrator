from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional

class DatabaseSettings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    
    def get_database_url(self) -> str:
        db_url = (
            f"mysql+mysqlconnector://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )
        print(f"Database URL for connection -> {db_url}")
        return db_url
    
database_settings = DatabaseSettings() # type: ignore

engine = create_engine(database_settings.get_database_url(),
                       pool_recycle=7200,
                       echo=True,
                       pool_size=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
