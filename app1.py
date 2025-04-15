from fastapi import FastAPI,UploadFile,File,Form,Depends
from pydantic import BaseModel,HttpUrl
from typing import Optional

app=FastAPI()
employees={
    1:{"name": "Tim", "age": 22,"year": 2003},
    2:{"name":"jeena","age":25,"year":2000}
}
class EmployeeModel(BaseModel):
    # employees_id:int
    name:str
    age:int
    year:int
    # avatar:HttpUrl

class UpdateEmployeeModel(BaseModel):
    # employees_id:int
    name:Optional[str]=None
    age:Optional[int]=None
    year:Optional[int]=None

@app.get("/")
def root():
    return {"Message":"First Data"}

@app.get("/get-employees/{employees_id}")
def get_data(employees_id:int):
    return employees.get(employees_id,{"Error": "employees not found"})

@app.get("/get-employee")
def get_employee(name:Optional[str],age:Optional[int]):
    for employees_id in employees:
        if employees[employees_id]["name"]==name:
            return employees[employees_id]
        if employees[employees_id]["age"]==age:
            return employees[employees_id]
    return "data not found"

# @app.post("/create-employees/")
# def create_employees(employee:EmployeeModel):
#     if employee.employees_id in employees:
#         return {"Error":"already exists"}
#     employees[employee.employees_id]=employee.dict()
#     return employee

# @app.post("/create-employees/")
# def create_employees(employee:EmployeeModel):
#     if employee.name in employees:
#         return {"Error":"already exists"}
#     employees[employee.name]={"name":employee.name,"age":employee.age,"year":employee.year,"avatar":employee.avatar}
#     return employee


def as_form(name: str = Form(...),age: int = Form(...),year: int = Form(...)) -> EmployeeModel:
    return EmployeeModel(name=name, age=age, year=year)

@app.post("/create-employees/")
def create_employees(employee: EmployeeModel = Depends(as_form),avatar:UploadFile=File(...)):
    if employee.name in employees:
        return {"Error":"already exists"}
    employees[employee.name]={"name":employee.name,"age":employee.age,"year":employee.year,"avatar":avatar.filename}
    return {"success":employees}

import os
from fastapi.responses import FileResponse
@app.get("/get-image/{image_name}")
def get_image(image_name:str):
    image_path,ext=os.path.join("image",image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path,media_type="image")
    return "Image is not found"




@app.put("/update-employee/{employees_id}")
def update_employee(employees_id:int, employee: UpdateEmployeeModel):
    if employees_id not in employees:
        return "Employees does not exists"
    if employees_id is not None:
        employees[employees_id]["name"]=employee.name
    if employees_id is not None:
        employees[employees_id]["age"]=employee.age
    if employees_id is not None:
        employees[employees_id]["year"]=employee.year
    return employees[employees_id]

# @app.put("/update-employee/")
# def update_employee(employee: UpdateEmployeeModel):
#     if employee.employees_id not in employees:
#         return "Employees does not exists"
#     if employee.employees_id is not None:
#         employees[employee.employees_id]["name"]=employee.name
#     if employee.employees_id is not None:
#         employees[employee.employees_id]["age"]=employee.age
#     if employee.employees_id is not None:
#         employees[employee.employees_id]["year"]=employee.year
#     return employees[employee.employees_id]

@app.put("/update-employee/")
def update_employee(employee: UpdateEmployeeModel):
    for emp_id, emp_data in employees.items():
        if emp_data["name"] == employee.name:
            if employee.age is not None:
                emp_data["age"] = employee.age
            if employee.year is not None:
                emp_data["year"] = employee.year
            return emp_data
    return {"Error": "Employee does not exist"}

# @app.delete("/delete-employees/{employees_id}")
# def delete_employee(employees_id:int):
#     if employees_id not in employees:
#         return "employee does not exist"
#     del employees[employees_id]


@app.delete("/delete-employees/")
def delete_employee(employee: UpdateEmployeeModel):
    for emp_id in employees.keys():
        if employees[emp_id]["name"] == employee.name:
            del employees[emp_id]
            return "employee is deleted"
    return "employee does not exist"





# class usermodel(BaseModel):
#     name:str
#     email:str
# @app.post("/upload-avatar")
# def upload_avatar(image:UploadFile=File("C:\Users\91773\OneDrive\Desktop\fastapi\avatar-profile-vector-illustrations-website-social-networks-user-profile-icon_495897-224.avif")):
    