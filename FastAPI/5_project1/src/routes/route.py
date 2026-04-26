from fastapi import APIRouter 


router = APIRouter() 

@router.get("/") 
def home(): 
    return { "status":"success" , "messages": "Everything Fine" }