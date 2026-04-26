from dotenv import load_dotenv 
import os 
load_dotenv(dotenv_path=".env") 

class Settings: 
    SECREATE_KEY = os.environ["SECREATE_KEY"] 
    ALGORITHM=os.environ["ALGORITHM"] 
    ACCESS_EXPIRATION_TOKEN=os.environ["ACCESS_EXPIRATION_TOKEN"] 


config = Settings()