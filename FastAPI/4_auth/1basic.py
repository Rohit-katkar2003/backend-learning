from fastapi import FastAPI , Depends , HTTPException  , Request
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from jose import jwt , JWTError 
from passlib.context import CryptContext
from datetime import datetime , timedelta 
import time
import hashlib
app = FastAPI(title="Production Auth system") 

# ─────────────────────────────────────────
# CONFIG
# In real life → load from .env with python-dotenv
# NEVER hardcode secrets in production!
# ─────────────────────────────────────────
SECRETE_KEY="supersecreatekey"   ## keep this in os.environ["SCREATE_KEY"] 
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRATION_MIN = 20 

fake_user_db = {} 


# sha256_crypt has no 72-byte limit like bcrypt
# In prod you'd use argon2 — strongest available
## password hashing 
pwd_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto",
    bcrypt__truncate_error=False  # suppress the error, bcrypt handles truncation internally
)
security = HTTPBearer() 

# ====================
# ─────────────────────────────────────────
# MIDDLEWARE — runs on EVERY request
# Before call_next  → runs on incoming request
# After  call_next  → runs on outgoing response
# ─────────────────────────────────────────
# ====================
@app.middleware("http")
async def log_middleware(request:Request , call_next):
    start_time = time.time()
    print(f"\n➡️ Incoming request: {request.method} {request.url}")

    response = await call_next(request)   #  # ← your actual route runs here 
    process_time = time.time() - start_time
    print(f"⬅️ Completed in {process_time:.4f}s with status {response.status_code}\n")

     # You can also add response headers here, e.g.:
    # response.headers["X-Process-Time"] = str(duration)
    return response



## password functionality 
def _prepare(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()  # always 64 chars

def hash_password(password: str) -> str:
    return pwd_context.hash(_prepare(password))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_prepare(plain_password), hashed_password)
#========================
## jwt token 
#=============================

def create_token(data:dict): 
    print("🎟️Creating jwt Token.....")
    to_encode = data.copy() 
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MIN) 
    to_encode.update({"exp":expire})  
    token = jwt.encode(to_encode , SECRETE_KEY , algorithm=ALGORITHM) 
    print("✅ Token created: ", token) 
    return token 


def decode_token(token:str): 
    print("🌿 Decoding Token .... ")
    try: 
        payload = jwt.decode(token , SECRETE_KEY , algorithms=ALGORITHM)
        print(f"Payload : {payload}")
        return payload 
    except JWTError: 
        print("Invalid Token... ")
        return None   
    
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)): 
    """
    This is a FastAPI dependency.
    Any route that does `user=Depends(get_current_user)` will:
    1. Require a Bearer token in the Authorization header
    2. Decode it and return the payload as `user`
    3. Auto-reject with 401 if token is missing or invalid
    """
    print("🔐 Checking current user...")

    token = credentials.credentials 
    payload = decode_token(token) 
    
    if payload is None: 
        raise HTTPException(status_code=401 , detail="Invalid Token") 
    
    return payload 

# =========================
## Routes
# ========================= 
@app.get("/")
def home():
    return {"messages":"Auth System Running.... "} 

## sign-up 
@app.post("/signup")
def signup(username:str , password:str , role:str="user"): 
    print("Signup request...") 

    if username in fake_user_db: 
        raise HTTPException(status_code=400 , detail="user exists") 
    
    hashed = hash_password(password) 
    # print("hashed_password : " , hashed) 

    fake_user_db[username] = {
        "username" : username , 
        "password": hashed , 
        "role" : role
    } 

    print("✅  user stored : ", fake_user_db) 
    return {"message":"User created"} 


## Login
@app.post("/login")
def login(username:str , password:str): 
    print("Login request... ")
    user = fake_user_db.get(username) 
    if not user: 
        raise HTTPException(status_code=404 , detail="User not Found")

    if not verify_password(password , user['password']): 
        raise HTTPException(status_code=401 , detail="wrong password") 
    
    token = create_token({
        "username":username , 
        "role":user["role"]
    }) 

    return {"access token": token} 

@app.get("/profile")
def profile(user=Depends(get_current_user)):
    print("👤 Accessing profile...")
    return {"message": "User profile", "user": user}


# -------------------------
# ADMIN ROUTE (RBAC)
# -------------------------
@app.get("/admin")
def admin(user=Depends(get_current_user)):
    print("🛡️ Admin check...")

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return {"message": "Welcome Admin 👑"}


# =========================
# 🔑 OAUTH (SIMULATION)
# =========================
# ─────────────────────────────────────────
# OAUTH SIMULATION
# Real flow: redirect → Google → code → token exchange → get user info
# Libraries to use for real OAuth: authlib, python-social-auth
# ─────────────────────────────────────────
@app.get("/oauth/login")
def oauth_login():
    # In real life you'd build a URL with client_id, redirect_uri, scope, state
    return {
        "message": "Redirect user to this URL",
        "url": "https://accounts.google.com/o/oauth2/auth?client_id=YOUR_ID&..."
    }

@app.get("/oauth/callback")
def oauth_callback():
    # Real flow: receive ?code=... from Google, POST to token endpoint, get user info
    # Here we just simulate a Google user coming back
    google_user = {"email": "google_user@gmail.com", "name": "Google User"}
    token = create_token({"username": google_user["email"], "role": "user"})
    return {"message": "OAuth login success", "access_token": token}


if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(app , host="0.0.0.0" , port=8000)