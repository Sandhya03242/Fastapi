# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}



# from typing import Union

# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
# #     return {"item_id": item_id, "q": q}


# # @app.put("/items/{item_id}")
# # def update_item(item_id: int, item: Item):
# #     return {"item_name": item.price, "item_id": item_id}



# from fastapi import FastAPI
# from fastapi import Path
# from pydantic import BaseModel
# from typing import Optional
# app=FastAPI()

# students={1:{"name":"sandhya","age":"22"},2:{"name":"Tina","age":"23"}}
# class studentmodel(BaseModel):
#     name: str
#     age:int

# @app.get("/")
# def root():
#     return {"Name":"First Data"}

# @app.get("/get-student/{student_id}")
# def get_student(student_id:int = Path(...,description="The ID of student you want to view")):
#     return students[student_id]

# @app.get("/get-by-name/{student_id}")
# def  get_student(*,student_id:int,name:Optional[str]=None,test:int):
#     for student_id in students:
#         if students[student_id]["name"]==name:
#             return students[student_id]
#     return {"Data":"Not found"}
        
# @app.post("/create-student/{student_id}")
# def create_students(student_id:int,student:studentmodel):
#     if student_id in students:
#         return {"Error":"Student exists"}
#     student[student_id]=students
#     return students[student_id]




# from enum import Enum
# from fastapi import FastAPI, Path
# class Model_Name(str,Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"
# app=FastAPI()
# @app.get("/models/{model_name}")
# def get_model(model_name:Model_Name=Path(...,description="Select a Model Name")):
#     if model_name in Model_Name.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}
#     if model_name.value=="lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


# from fastapi import FastAPI

# app = FastAPI()

# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# from fastapi import FastAPI
# from pydantic import BaseModel


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# app = FastAPI()


# @app.post("/items/")
# async def create_item(item: Item):
#     return item




from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

students = {
    1: {"name": "sandhya", "age": 22},
    2: {"name": "Tina", "age": 23}
}

class StudentModel(BaseModel):
    name: str
    age: int

class UpdateStudentModel(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None

@app.get("/")
def root():
    return {"Name": "First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of student you want to view")):
    return students.get(student_id, {"Error": "Student not found"})

@app.get("/get-by-name")
def get_student_by_name(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}

@app.post("/create-student/{student_id}")
def create_students(student_id: int, student: StudentModel):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id] = student 
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudentModel):
    if student_id not in students:
        return {"Error":"Student does not exists"}
    if student.name!=None:
        students[student_id]["name"] = student.name
    if student.age!=None:
        students[student_id]["age"] = student.age
    return students[student_id]
@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id  not in students:
        return {"error":"student does not exist"}
    del students[student_id]