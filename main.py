#Python
from enum import Enum
from typing import Optional
#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastApI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Path, Query


app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Sergio"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Torres"
        )
    age: int = Field(
        ...,
        gt=0,
        le=130,
        example=25
        )
    hair_color: Optional[HairColor] = Field(default=None, example="black")

    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):

    password: str = Field(..., min_length=8)

    # class Config:
    #     schema_extra = {
    #         "example":{
    #             "first_name": "Sergio",
    #             "last_name": "Romero",
    #             "age": 29,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }

class PersonOut(PersonBase):
    pass

@app.get("/", status_code=status.HTTP_200_OK)  # path operation decorator
def home():  # path operation function
    return {"Hello": "World"}

# Request and Response body
@app.post("/person/new",response_model=PersonOut,status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    """Los ... en fastapi significa que son obligatorios"""
    return person

#validaciones: Query parameters
@app.get("/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Sergio"
        ),
    age: str = Query(# no es lo ideal. lo ideal es que query parameter sea optional
        ...,
        title="Person Age",
        description="this is the person age. It's required",
        example=25
        ) 
    ):
    return {name:age}

#Validaciones: path parameters
@app.get("/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(...,
    gt=0,
    title="Person id",
    description="This is the person id. It must be greater than 0",
    example=123
    )
    ):
    return {person_id: "It exists!"}

#Validaciones : Request Body
@app.put("/person/{person_id}", status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person:  Person = Body(...),
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())

    # return results
    return person
