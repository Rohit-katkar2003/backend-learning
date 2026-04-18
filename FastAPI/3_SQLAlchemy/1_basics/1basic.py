
from sqlalchemy import create_engine  , text

engine = create_engine(url="sqlite:///Mydatabase.db" , ## here u paste ur database link whether it is sqlite,postgres, sql
                       echo=True) ## echo for the debugging 

conn = engine.connect() 

conn.execute(text("create table if not exists People(name str , age int)")) 

conn.commit() 


from sqlalchemy.orm import Session ## it is same as engine.connect() it another trick as a session 
session = Session(engine) 

name = "Rohit" 
age = 22 
session.execute(text(f"INSERT into people(name , age) values('{name} ', {age})")) 

session.commit() 



## the above way is not correct to write the Query we use the different way you can see in 2basic.py