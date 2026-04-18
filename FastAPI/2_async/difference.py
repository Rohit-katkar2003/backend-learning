import asyncio 
import time 


def task1():
    print("Start")
    time.sleep(5)  # waits
    print("End")



async def task():
    print("Start")
    await asyncio.sleep(5)  # doesn't block
    print("End") 


async def main():
    await asyncio.gather(
        task(),
        task(),
        task()
    )

if __name__ == "__main__": 
    str_t= time.time() 
    task1() 
    print(f"sync function time : {time.time()-str_t}") 

    print("----------------------------------")
    str_t =time.time() 
    asyncio.run(task())   ## here we got 5 means same then what is difference see main
    print(f"Async function time : {time.time() - str_t}") 

    print("==================================")
    str_t= time.time() 
    asyncio.run(main()) 
    print(f"Async function in parallel time : {time.time()-str_t}") 