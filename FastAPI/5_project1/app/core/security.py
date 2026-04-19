"All JWT and password logic lives here. Nothing else touches these details:" 

from datetime import timedelta , datetime 
from jose import jwt , JWTError 
from passlib.context import CryptContext 
from app.core.config import settings 

pwd_context = CryptContext(schemes=['bcrypt'] , deprecated="auto") 

## password
def hash_password(password:str): 
    return pwd_context.hash(password) 

def verify_password(plain:str ,hashed:str): 
    return pwd_context.verify(plain , hashed) 

## jwt 
def create_token(data:dict): 
    payload = data.copy() 
    payload['exp'] = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 
    payload["type"] = "access"           # ← tag the token type!
    return jwt.encode(payload , settings.SECRET_KEY , algorithm=settings.ALGORITHM) 

def create_refresh_token(data:dict): 
    payload = data.copy() 
    payload['exp'] = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS) 
    payload["type"] = "refresh"           # ← tag the token type!
    return jwt.encode(payload , settings.SECRET_KEY , algorithm=settings.ALGORITHM) 

def decode_token(token:str): 
    try: 
        return jwt.decode(token , settings.SECRET_KEY , algorithms=settings.ALGORITHM)
    except JWTError: 
        return None 


"""
Why bcrypt? It's slow by design — resistant to brute‑force.
JWT payload: we'll store {"sub": user.email}.

---------------------------------------------------------------

Notice we tag tokens with "type": "access" or "type": "refresh". 
This means you can reject someone who tries to use a refresh token on a protected 
route and vice versa — a real security detail most tutorials skip.
"""