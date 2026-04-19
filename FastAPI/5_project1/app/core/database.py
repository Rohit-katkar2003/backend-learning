from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession  
from sqlalchemy.orm import   declarative_base 
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL , echo=True , future=True)  

#async session factory 
AsyncSessionLocal = async_sessionmaker(
    engine , 
    class_=AsyncSession , 
    expire_on_commit=False   # Prevents expired objects after commit (async behaviour)
)

# base class for ORM Model 
Base = declarative_base() 


# get the db session (we use in route) 

async def get_db() -> AsyncSession: 
    async with AsyncSessionLocal()  as session: 
        yield session 



"""Key Points:

create_async_engine uses aiosqlite under the hood because URL starts with sqlite+aiosqlite:///.

async_sessionmaker produces AsyncSession objects.

expire_on_commit=False is recommended in async SQLAlchemy to avoid unexpected lazy loads.

get_db is a FastAPI dependency that provides a session per request and closes it automatically.

"""



