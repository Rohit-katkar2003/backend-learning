from pydantic import BaseModel 


class AddStudent(BaseModel): 
    id: int
    name: str 
    email:str 
    age: int
    city : str = "Sambhaji-Nagar"
    is_active : bool = True