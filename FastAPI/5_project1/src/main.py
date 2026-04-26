from .routes.route import router 
from fastapi.middleware.cors import CORSMiddleware 
from fastapi import FastAPI  , Request , Depends , HTTPException


app = FastAPI(title="School backend ....! " ,debug=True) 

app.add_middleware(
    CORSMiddleware , 
    allow_origins = ["*"] , 
    allow_credentials = True , 
    allow_methods = ["*"] , 
    allow_headers = ["*"]
)

@app.middleware("http")
async def log_middleware(request:Request , class_next): 
    


app.include_router(router) 


