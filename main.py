from fastapi import FastAPI  #Importing FastAPI class from fastapi module

app = FastAPI() #Creating an instance of FastAPI class

"""First Step"""
@app.get("/") #Defining a route for the root path. A "path" is also commonly called an "endpoint" or a "route".
async def root(): #`root` function will be called when the root path is accessed
    return {"message": "Hello World"} #`root` function returns a dictionary with a key `message` and value `Hello World`



"""
    Path Parameters
    You can declare path "parameters" or "variables" with the same syntax used by Python format strings:
    """
@app.get("/items/{item_id}")
async def read_item(item_id: int): #You can declare the type of a path parameter in the function, using standard Python type annotations:
    return {"item_id": item_id}

#Predefined values for path parameters
from enum import Enum #Importing Enum class from enum module

class ModelName(str, Enum): #Create class attributes with fixed values, which will be the available valid values
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName): #Create a path parameter with a type annotation using the enum class you created (ModelName):
    if model_name is ModelName.alexnet: #You can compare the value of the path parameter with the enumeration member in your created enum ModelName:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet": #You can get the actual value (a str in this case) using model_name.value, or in general, your_enum_member.value:
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

#Because the available values for the path parameter are predefined, the interactive docs can show them nicely:


"""
    Query Parameters
    When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
    Query parameters are optional parameters that you can pass to the API. They are separated from the path parameters by a `?`, and multiple query parameters are separated by a `&`.
    """

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items2/") 
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.
#http://127.0.0.1:8000/items/?skip=0&limit=10

#Optional parameters
@app.get("/items2/{item_id}")
async def read_item(item_id: str, q: str | None = None): #The function parameter q will be optional, and will be None by default
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

#Query parameter type conversion
#You can also declare bool types, and they will be converted:
#http://127.0.0.1:8000/items3/2?q=leo&short=true
@app.get("/items3/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#Multiple path and query parameters
#You can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which.
#And you don't have to declare them in any specific order.
#They will be detected by name:
#http://127.0.0.1:8000/users/3/items/3?q=4&short=false
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#Required query parameters
#To make a query parameter required, you can just not declare any default value:
#http://127.0.0.1:8000/items4/4?needy=yes
@app.get("/items4/{item_id}")
async def read_user_item(item_id: str, needy: str): #Here the query parameter needy is a required query parameter of type str
    item = {"item_id": item_id, "needy": needy}
    return item

#Required and default query parameters
#http://127.0.0.1:8000/items5/5?needy=yes&skip=5&limit=100
@app.get("/items5/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

#In this case, there are 3 query parameters:
#needy, a required str.
#skip, an int with a default value of 0.
#limit, an optional int.


"""
    Request Body
    A request body is data sent by the client to your API. A response body is the data 
    your API sends to the client. FastAPI uses Pydantic models to define the request body.
    """

from pydantic import BaseModel #Importing BaseModel class from pydantic module

class Item(BaseModel): #Declare your data model as a class that inherits from BaseModel.
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

#The same as when declaring query parameters, when a model attribute has a default value,
#  it is not required. Otherwise, it is required. Use None to make it just optional.

@app.post("/items/")
async def create_item(item: Item):
    return item

#Use the model
@app.post("/items2/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

#Request body + path parameters
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()} #The ** operator is used to unpack dictionaries.

#Request body + path + query parameters
@app.put("/item2/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


"""Query Parameters and String Validations"""

#http://127.0.0.1:8000/items6/?q=leo
@app.get("/items6/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Additional validation

#We are going to enforce that even though q is optional,
#whenever it is provided, its length doesn't exceed 50 characters.

from typing import Annotated #Annotated from typing module
from fastapi import  Query #Importing Query class from fastapi module

@app.get("/items7/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Add more validations
#http://127.0.0.1:8000/items8/?q=leo
@app.get("/items8/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Add regular expressions

#You can define a regular expression pattern that the parameter should match:
#Before Pydantic version 2 and before FastAPI 0.100.0, the parameter was called regex instead of pattern, but it's now deprecated.
#http://127.0.0.1:8000/items9/?q=fixedquery
@app.get("/items9/")
async def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#This specific regular expression pattern checks that the received parameter value:
#^: starts with the following characters, doesn't have characters before.
#fixedquery: has the exact value fixedquery.
#$: ends there, doesn't have any more characters after fixedquery.

#Default values
@app.get("/items10/")
async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Required parameters

#http://127.0.0.1:8000/items11/?q=leo
@app.get("/items11/")
async def read_items(q: Annotated[str, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Required, can be None

#http://127.0.0.1:8000/items12/?q=none
@app.get("/items12/")
async def read_items(q: Annotated[str | None, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Query parameter list / multiple values

#When you define a query parameter explicitly with Query you can also
# declare it to receive a list of values, or said in another way, to receive multiple values.
#http://localhost:8000/items13/?q=foo&q=bar
@app.get("/items13/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items
#To declare a query parameter with a type of list, like in the example above, 
# you need to explicitly use Query, otherwise it would be interpreted as a request body.

#Query parameter list / multiple values with defaults
@app.get("/items14/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items

#Declare more metadata (Title,description,alias,deprecated)
@app.get("/items15/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#http://localhost:8000/items16/?item-query=leo
@app.get("/items16/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Deprecating parameters
@app.get("/items17/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Exclude parameters from OpenAPI
@app.get("/items18/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}

#Custom Validation
#There could be cases where you need to do some custom validation 
# that can't be done with the parameters shown above.
#In those cases, you can use a custom validator function that is applied after the normal
# validation (e.g. after validating that the value is a str).
#You can achieve that using Pydantic's AfterValidator inside of Annotated.
import random
from pydantic import AfterValidator 
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}
def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

#http://localhost:8000/items19/?id=isbn-9781439512982
@app.get("/items19/")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}





