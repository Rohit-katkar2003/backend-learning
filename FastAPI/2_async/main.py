##  Here we do API can handle 100k requests at a time 

import asyncio 
from fastapi import FastAPI 
import uvicorn 

app = FastAPI() 

async def fake_req(): 
    await asyncio.sleep(0.01) ## non blocking 
    return {"status" : "ok"} 


@app.get("/")
async def root(): 
    response = await fake_req() 
    return response 

@app.get("/multi")
async def multi_req(): 
    response = [ fake_req() for _ in range(10)] 
    result = await asyncio.gather(*response) 
    return {"result":result}  

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)