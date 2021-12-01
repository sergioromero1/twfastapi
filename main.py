#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FastApI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Path
from fastapi import Query

app = FastAPI()

#Models
class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")  # path operation decorator
def home():  # path operation function
    return {"Hello": "World"}

# Request and Response body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    """Los ... en fastapi significa que son obligatorios"""
    return person

#validaciones: Query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(# no es lo ideal. lo ideal es que query parameter sea optional
        ...,
        title="Person Age",
        description="this is the person age. It's required"
        ) 
    ):
    return {name:age}

#Validaciones: path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(...,
    gt=0,
    title="Person id",
    description="This is the person id. It must be greater than 0"
    )
    ):
    return {person_id: "It exists!"}

#Validaciones : Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person:  Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    
    return results

