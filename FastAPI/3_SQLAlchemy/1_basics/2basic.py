from sqlalchemy import create_engine ,MetaData, Table , Column , Integer , String , Float  , insert , ForeignKey , func

engine =create_engine(url = "sqlite:///Mydata.db" ,
                      echo=True)


meta = MetaData() # it is For metadata 
""" By the Engine and metadata when we change db like postgres , SQL everything like querying and can be handle by this too things """

people = Table(
    "people"  ,  ## name of table
    meta ,    ## metadata
    Column("id" , Integer , primary_key=True) , 
    Column("name" , String , nullable=False) , 
    Column("age" , Integer)
)

# meta.create_all(engine) # write it after all the tables 
 

# conn = engine.connect() 

insert_statement = people.insert().values(id=1 , name="Rohit" , age=30) 

# # second way to insert 
# insert2 = insert(people).values(id=2 , name="akshay" , age=21)
# result = conn.execute(insert_statement) 
# conn.commit() 


## select statement 
# select_statement = people.select().where(people.c.age > 20) 
# result = conn.execute(select_statement)  
# for row in result.fetchall():
#     print(row)
# conn.commit()


## update statement 
# update_statement = people.update().where(people.c.id==1).values(age=22) 
# result = conn.execute(update_statement)  

# select_statement = people.select()
# result = conn.execute(select_statement)
# for row in result.fetchall():
#     print(row)
# conn.commit()
 

## delete statement 
# delete_statement = people.delete().where(people.c.id==1)
# result = conn.execute(delete_statement)
# select_statement = people.select()
# result = conn.execute(select_statement)
# for row in result.fetchall():
#     print(row)
# conn.commit()


############################## Now we add realtion of table with other table(Foreign Key) ##################################### 
things = Table(
    "things" , 
    meta , 
    Column("id" , Integer , primary_key=True) , 
    Column("description" , String  , nullable=False) , 
    Column("value" , Float) , 
    Column("owner" , Integer , ForeignKey("people.id"))  # adding foreing key of people.id column 
) 

meta.create_all(engine) 
conn = engine.connect()



def select_data(Table_NAME):  
    select_statement = Table_NAME.select()
    result = conn.execute(select_statement)
    for row in result.fetchall():
        print(row)
    conn.commit() 

## adding some more entries 
# insert_people = people.insert().values(
#     [
#         {"id":1 , "name":"Rohit" , "age":30} , 
#         {"id":2 , "name":"akshay" , "age":21} , 
#         {"id":3 , "name":"pravin" , "age":22} ,
#         {"id":4 , "name":"amol" , "age":23} , 
#         {"id":5 , "name":"pooja" , "age":26} , 
#         {"id":6 , "name":"akansha" , "age":30}  
#     ]
# )

# result = conn.execute(insert_people)
# conn.commit() 
# select_data(people)
 
# insert_things = things.insert().values(
#     [
#         {"owner":1 , "description" : "laptop" , "value":45000.0} , 
#         {"owner":2 , "description" : "pc" , "value":450000.0} , 
#         {"owner":6 , "description" : "keyboard" , "value":4500.0} , 
#         {"owner":1 , "description" : "Asus laptop" , "value":45000.0} , 
#         {"owner":3 , "description" : "car" , "value":500000.0} , 
#         {"owner":6 , "description" : "mouse" , "value":450.0} , 
#         {"owner":4 , "description" : "MSI" , "value":12000.0} , 

#     ]
# )
# result = conn.execute(insert_things)  
# conn.commit()
# select_data(things)  


# join_statement = people.join(things , people.c.id==things.c.owner) 
# select_statement = people.select().with_only_columns(people.c.name , things.c.description).select_from(join_statement) 
# result = conn.execute(select_statement)
# for row in result.fetchall(): 
#     print(row) 
# conn.commit()

## outer join 
# join_statement = people.outerjoin(things , people.c.id==things.c.owner) 
# select_statement = people.select().with_only_columns(people.c.name , things.c.description).select_from(join_statement) 
# result = conn.execute(select_statement)
# for row in result.fetchall(): 
#     print(row) 
# conn.commit()



############################################################ Group-by ######################################################

group_by_statement = things.select().with_only_columns(things.c.owner , func.sum(things.c.value)).group_by(things.c.owner) 
result = conn.execute(group_by_statement) 

for row in result.fetchall(): 
    print(row)

print("==== having statement =======")
## having
group_by_statement = things.select().with_only_columns(things.c.owner , func.sum(things.c.value)).group_by(things.c.owner).having(func.sum(things.c.value)> 50000)
result = conn.execute(group_by_statement) 

for row in result.fetchall(): 
    print(row)