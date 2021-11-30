#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FastApI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query

app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")  # path operation decorator
def home():  # path operation function
    return {"Hello": "World"}

#validaciones: Query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...) # no es lo ideal. lo ideal es que query parameter sea optional
    ):
    return {name:age}

# Request and Response body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    """Los ... en fastapi significa que son obligatorios"""
    return person
