#Python
from enum import Enum
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastApI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Cookie, File, Header, Path, Form, Query, UploadFile


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

class LoginOut(BaseModel):
    username: str= Field(...,max_length=20, example="miguel2021")

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

@app.get("/", status_code=status.HTTP_200_OK,tags=["Home"])  # path operation decorator
def home():  # path operation function
    return {"Hello": "World"}

# Request and Response body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the information in the database

    Parameters:
    - Request Body parameter:
        - **person: Person** -> A person model with first name , last name, age , hair color and marital status

    Returns a person model with first name , last name, age, hair color and marital status
    """
    return person

#validaciones: Query parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True
    )
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

persons = [1,2,3,4,5]
#Validaciones: path parameters
@app.get("/person/detail/{person_id}", status_code=status.HTTP_200_OK, tags=["Persons"])
def show_person(
    person_id: int = Path(...,
    gt=0,
    title="Person id",
    description="This is the person id. It must be greater than 0",
    example=123
    )
    ):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This persons doesn't exists!"
        )
    return {person_id: "It exists!"}

#Validaciones : Request Body
@app.put("/person/{person_id}", status_code=status.HTTP_200_OK,tags=["Persons"])
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

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons", "Login"]
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
   ):
    return user_agent

# Files

@app.post(
    path="/post-image",
    tags=["Image"]
)
def post_image(
    image: UploadFile = File(...)
    ):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024,ndigits=2)
    }