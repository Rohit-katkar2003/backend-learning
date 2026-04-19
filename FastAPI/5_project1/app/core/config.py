from pydantic_settings import BaseSettings 

class Settings(BaseSettings): 

    APP_NAME : str = "School Management system" 
    DEBUG: bool = False 
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # database 
    DATABASE_URL: str = "sqlite+aiosqlite:///./school.db"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7 

    class Config: 
        env_file = ".env"  # it tales pydantic where load from 
        case_sensitive=True  # DATABASE_URL != database_url 

settings = Settings() 

"""Why this matters: Instead of os.getenv("SECRET_KEY") scattered everywhere (and forgetting to handle None), you just do:
from app.core.config import settings
print(settings.SECRET_KEY)   # always a string, never None, validated at startup

If .env is missing DATABASE_URL, your app crashes at startup with a clear error — not in the middle of a request 3 hours later.
"""

