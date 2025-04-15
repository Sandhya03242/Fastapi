from fastapi import FastAPI, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse  # Changed from FileResponse
import os
from mangum import Mangum

app = FastAPI()

# Initialize employees dictionary
employees = {
    1: {"name": "Tim", "age": 22, "year": 2003},
    2: {"name": "jeena", "age": 25, "year": 2000}
}

class EmployeeModel(BaseModel):
    name: str
    age: int
    year: int

class UpdateEmployeeModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[int] = None

@app.get("/")
async def root():  # Made async
    return {"Message": "API is working"}

@app.get("/get-employees/{employees_id}")
async def get_data(employees_id: int):
    return employees.get(employees_id, {"Error": "Employee not found"})

@app.get("/get-employee")
async def get_employee(name: Optional[str] = None, age: Optional[int] = None):
    for employee in employees.values():
        if name and employee["name"] == name:
            return employee
        if age and employee["age"] == age:
            return employee
    return {"Error": "Data not found"}  # Return JSON instead of string

def as_form(name: str = Form(...), age: int = Form(...), year: int = Form(...)) -> EmployeeModel:
    return EmployeeModel(name=name, age=age, year=year)

@app.post("/create-employees/")
async def create_employees(employee: EmployeeModel = Depends(as_form), avatar: UploadFile = File(...)):
    if employee.name in [e["name"] for e in employees.values()]:
        return {"Error": "Employee already exists"}
    new_id = max(employees.keys()) + 1
    employees[new_id] = {
        "name": employee.name,
        "age": employee.age,
        "year": employee.year,
        "avatar": avatar.filename
    }
    return {"success": employees[new_id]}

# Temporarily disable image endpoint for Vercel deployment
# @app.get("/get-image/{image_name}")
# async def get_image(image_name: str):
#     image_path = os.path.join("image", image_name)
#     if os.path.exists(image_path):
#         return FileResponse(image_path, media_type="image/avif")
#     return {"Error": "Image not found"}

from fastapi.responses import FileResponse

@app.get("/get-image/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join("public", "image", image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/avif")
    return {"Error": "Image not found"}


@app.put("/update-employee/{employees_id}")
async def update_employee(employees_id: int, employee: UpdateEmployeeModel):
    if employees_id not in employees:
        return {"Error": "Employee does not exist"}
    if employee.name is not None:
        employees[employees_id]["name"] = employee.name
    if employee.age is not None:
        employees[employees_id]["age"] = employee.age
    if employee.year is not None:
        employees[employees_id]["year"] = employee.year
    return employees[employees_id]

@app.delete("/delete-employees/{employees_id}")
async def delete_employee(employees_id: int):
    if employees_id not in employees:
        return {"Error": "Employee does not exist"}
    del employees[employees_id]
    return {"Success": "Employee deleted"}

handler = Mangum(app,lifespan="off")