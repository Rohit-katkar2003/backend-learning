from fastapi import  APIRouter 
import json
from models import AddStudent
router = APIRouter() 

@router.get("/health")
def check(): 
    return {"status":"success" , "message":"the health of API-all good"} 


def read_js_data(json_path = "data.json"): 
    with open(json_path , "r") as f: 
        data  = json.load(f)
    return data 

def write_json(new_data , json_path = "data.json" ):  
    
    with open(json_path , "w" , encoding="utf-8") as f: 
        json.dump(new_data,f , indent=4 , ensure_ascii=False) 
    return "Data updated successfully. "

@router.get("/all_students")
async def all_students(): 
    try: 
        data = read_js_data() 
        return {"status":"success" , "message": data['users']} 
    
    except Exception as e: 
        return {"status":"Error" , "message":f"Got error {e}"} 
    
@router.post("/add_student")
async def add_student(stud  :AddStudent): 
    try: 
        data = read_js_data()
        new_data ={"id":stud.id , "name":stud.name , "email":stud.email , "age":stud.age ,"is_active":True}  
        print(new_data)
        data['users'].append(new_data)
        ans = write_json(data)
        return {"status":"success" , "message":ans} 
    
    except Exception as e: 
        return {"status":"Error" , "message":f"Got error {e}"} 
    
@router.delete("/delete_student/{student_id}")
async def delete_student(student_id:int):
    try:

        data = read_js_data() 
        Users = data.get("users" , []) 
        
        updated_users = [user for user in Users if user["id"] != student_id]  
    
        data["users"] = updated_users 
        if len(Users) == len(updated_users):
            return {"status": "error", "message": "Student not found"}

        write_json(data) 
        return {"status":"success" , "message":"successfully delete student."}

    except Exception as e: 
        return {"status":"Error" , "message":f"Got error {e}"} 
    

## when you want to update all the field 
@router.put("/")