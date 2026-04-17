from pydantic import BaseModel 
from typing import Optional 

class AddStudent(BaseModel): 
    id: int
    name: str 
    email:str 
    age: int
    city : str = "Sambhaji-Nagar"
    is_active : bool = True 


class UpdateStudent(BaseModel): 
    id: Optional[int]  = None
    name: Optional[str] = None
    email:Optional[str] = None
    age: Optional[int]  = None
    city : Optional[str] = "Sambhaji-Nagar"
    is_active : Optional[bool] = True