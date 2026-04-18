from sqlalchemy import create_engine , Integer , String , Column , Table , Float  , ForeignKey
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

    things = relationship("Thing", back_populates='person')

class Things(Base): 
    __tablename__ = "things" 
    id = Column(Integer , primary_key=True) 
    description = Column(String , nullable=True) 
    value = Column(Float )  
    owner = Column(Integer , ForeignKey("people.id"))  

    # person = relationship("Person", back_populates='things') 

Base.metadata.create_all(engine) 

session = sessionmaker(bind=engine) 
session = session() 

new_person = 
