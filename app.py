from fastapi import FastAPI,UploadFile,File,Form,Depends
from pydantic import BaseModel,HttpUrl
from typing import Optional
from fastapi.responses import FileResponse
import os
from mangum import Mangum

app=FastAPI()
employees={
    1:{"name": "Tim", "age": 22,"year": 2003},
    2:{"name":"jeena","age":25,"year":2000}}

class EmployeeModel(BaseModel):
    name:str
    age:int
    year:int

class UpdateEmployeeModel(BaseModel):
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

def as_form(name: str = Form(...),age: int = Form(...),year: int = Form(...)) -> EmployeeModel:
    return EmployeeModel(name=name, age=age, year=year)

@app.post("/create-employees/")
def create_employees(employee: EmployeeModel = Depends(as_form),avatar:UploadFile=File(...)):
    if employee.name in employees:
        return {"Error":"already exists"}
    employees[employee.name]={"name":employee.name,"age":employee.age,"year":employee.year,"avatar":avatar.filename}
    return {"success":employees}

@app.get("/get-image/{image_name}")
def get_image(image_name:str):
    image_path=os.path.join("image",image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path,media_type="image/avif")
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


@app.delete("/delete-employees/{employees_id}")
def delete_employee(employees_id:int):
    if employees_id not in employees:
        return "employee does not exist"
    del employees[employees_id]



handler = Mangum(app)
