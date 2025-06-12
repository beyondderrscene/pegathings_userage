from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from collections import defaultdict

app = FastAPI()

class item(BaseModel):
    name: str
    age: int
    initial: str = ""

class entry:
    def __init__(self):
        self.sum = 0
        self.freq = 0

lib = []
numlib = defaultdict(entry)

for i in lib:
    numlib[i.initial].sum += i.age
    numlib[i.initial].freq += 1

@app.get("/")
def home():
    return {"message":"Hello!"}

# POST - add user and age
@app.post("/add/")
def add_user(user: item):
    user.name = user.name.capitalize()
    user.initial = user.name[0]
    lib.append(user)
    numlib[user.initial].sum += user.age
    numlib[user.initial].freq += 1
    return {"message": f"User {user.name} added succesfully!"}    

# DELETE - delete by name
@app.delete("/delete/")
def delete_user(name: str):
    name = name.capitalize()
    for curr in lib:
        if(curr.name == name):
            numlib[curr.initial].sum -= curr.age
            numlib[curr.initial].freq -= 1
            lib.remove(curr)
            return {"message": f"{name} removed successfully!"}
    return {"message": f"User {name} not found."}

# GET - show current added users
@app.get("/show/")
def show_list():
    if(len(lib) == 0):
        return {"message": "No users in the library."}
    else:
        return {"Users":[f"name: {curr.name}, age: {curr.age}, initial: {curr.initial}" for curr in lib]}

# POST - add users from .csv
@app.post("/add_csv/")
def add_user_from_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    for _,row in df.iterrows():
        temp = item(name = row["Name"].capitalize(), age = row["Age"], initial = row["Name"].capitalize()[0])


# GET - get average age according to initial group
@app.get("/avg/{initial}")
def get_average(initial: str):
    initial = initial.capitalize()
    if(len(initial) != 1 or not("A" <= initial <= "Z")):
        return {"message": "Invalid char or len."}
    elif(numlib[initial].freq == 0):
        return {"message": f"No users of initial {initial} is recorded."}
    else:
        return {"message": f"Average of initial {initial} = {numlib[initial].sum / numlib[initial].freq}."}