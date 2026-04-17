from routes import router 
from fastapi import FastAPI 

app = FastAPI(title="API for Schools ERP" , summary="the API for School erp where ALL crud happens" , version="0.1.0")
app.include_router(router)

if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(app , host="0.0.0.0" , port=9999) 