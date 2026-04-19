from sqlalchemy import create_engine , Integer , String , Column , Table , Float  , ForeignKey , func
from sqlalchemy.orm import declarative_base , sessionmaker , relationship  
"""declarative base is the replacement of the metadata,Table as we do in 2basic.py 
"""
engine = create_engine("sqlite:///main.db" ,echo=True)

Base = declarative_base() 

class Person(Base): 
    __tablename__ = "people" 
    id = Column(Integer , primary_key=True) 
    name = Column(String , nullable=True) 
    age = Column(Integer)  

    things = relationship("Things", back_populates='person')

class Things(Base): 
    __tablename__ = "things" 
    id = Column(Integer , primary_key=True) 
    description = Column(String , nullable=True) 
    value = Column(Float )  
    owner = Column(Integer , ForeignKey("people.id"))  

    person = relationship("Person", back_populates='things') 

Base.metadata.create_all(engine) 

session = sessionmaker(bind=engine) 
session = session() 

# new_person = Person(name="sam" , age=80)  

# new_person = Person(name="charlie" , age = 20) 
# session.add(new_person) 

# new_thing = Things(description="camera" , value=300.0 , owner=new_person.id) 
# session.add(new_thing)
# session.commit()


################################# DB operations ################################## 

result = session.query(Person).all() 
print([p.name for p in result])

## here we don't use the where for conditions here we use filter  function 

result = session.query(Person).filter(Person.age >30).all() 
print([(r.name , r.age) for r in result])  


result = session.query(Person).filter(Person.id==1).update({"name":"sammy"})
session.commit()
print([result])  

# new_person = Person(name="amitabh" , age = 65) 
# thing1 = Things(description="Laptop", value=50000)
# thing2 = Things(description="Mouse", value=500)

# new_person.things.append(thing1)
# new_person.things.append(thing2)

# session.add(new_person) 
# session.commit()
## joins 
result = session.query(Person.name , Things.description).join(Things).all() 
print(result)  



## groupby 
result = session.query(Person.name , func.sum(Things.value)).group_by(Things.id).all() 
print(result)

result = session.query(Person.name , func.sum(Things.value)).group_by(Things.id).having(func.sum(Things.value)>1000.0).all() 
print(result)