from sqlalchemy import create_engine , Integer , String , Column , Table , Float  , ForeignKey , func
from sqlalchemy.orm import declarative_base , sessionmaker , relationship  
import pandas as pd 

engine = create_engine("sqlite:///main.db" ,echo=True)

df = pd.read_sql("SELECT * from people" , con=engine) 

print(df) 

# new_data = pd.DataFrame({"name":["rohit","pooja","yogesh","om","sanket"] , 
#                          "age":[22,26,24,19,20]}) 

# new_data.to_sql("people" , con=engine , if_exists="append" , index=False) 