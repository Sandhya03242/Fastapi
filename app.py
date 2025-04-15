from fastapi import FastAPI, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse, FileResponse
from mangum import Mangum
import os

app = FastAPI()

# Sample in-memory employee data
employees = {
    1: {"name": "Tim", "age": 22, "year": 2003},
    2: {"name": "Jeena", "age": 25, "year": 2000}
}

# Employee data model
class EmployeeModel(BaseModel):
    name: str
    age: int
    year: int

# For partial updates
class UpdateEmployeeModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[int] = None

# Home route
@app.get("/")
async def root():
    return {"Message": "API is working"}

# Get employee by ID
@app.get("/get-employees/{employee_id}")
async def get_employee_by_id(employee_id: int):
    employee = employees.get(employee_id)
    if employee:
        return employee
    return JSONResponse(status_code=404, content={"Error": "Employee not found"})

# Get employee by name or age
@app.get("/get-employee")
async def get_employee(name: Optional[str] = None, age: Optional[int] = None):
    for employee in employees.values():
        if name and employee["name"].lower() == name.lower():
            return employee
        if age and employee["age"] == age:
            return employee
    return JSONResponse(status_code=404, content={"Error": "Employee not found"})

# Dependency to receive form data as a Pydantic model
def as_form(
    name: str = Form(...), age: int = Form(...), year: int = Form(...)
) -> EmployeeModel:
    return EmployeeModel(name=name, age=age, year=year)

# Create a new employee
@app.post("/create-employees/")
async def create_employee(
    employee: EmployeeModel = Depends(as_form), avatar: UploadFile = File(...)
):
    if employee.name.lower() in [e["name"].lower() for e in employees.values()]:
        return JSONResponse(status_code=400, content={"Error": "Employee already exists"})

    new_id = max(employees.keys()) + 1
    employees[new_id] = {
        "name": employee.name,
        "age": employee.age,
        "year": employee.year,
        "avatar": avatar.filename
    }
    return {"Success": employees[new_id]}

# Serve image files from public/image directory
@app.get("/get-image/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join("public", "image", image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/avif")
    return JSONResponse(status_code=404, content={"Error": "Image not found"})

# Update an existing employee
@app.put("/update-employee/{employee_id}")
async def update_employee(employee_id: int, employee: UpdateEmployeeModel):
    if employee_id not in employees:
        return JSONResponse(status_code=404, content={"Error": "Employee not found"})

    if employee.name is not None:
        employees[employee_id]["name"] = employee.name
    if employee.age is not None:
        employees[employee_id]["age"] = employee.age
    if employee.year is not None:
        employees[employee_id]["year"] = employee.year

    return {"Updated": employees[employee_id]}

# Delete an employee
@app.delete("/delete-employee/{employee_id}")
async def delete_employee(employee_id: int):
    if employee_id not in employees:
        return JSONResponse(status_code=404, content={"Error": "Employee not found"})
    del employees[employee_id]
    return {"Success": f"Employee with ID {employee_id} deleted"}

# Required for AWS Lambda / Vercel
handler = Mangum(app, lifespan="off")
