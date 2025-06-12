from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from collections import defaultdict

from models import Base
from database import engine
Base.metadata.create_all(bind=engine)

app = FastAPI()

lib = pd.DataFrame(columns=["Name", "Age", "Initial"])

@app.get("/")
def home():
    return {"message":"Hello!"}

# POST - add user and age
@app.post("/add/")
def add_user(name: str, age: int):
    global lib
    name = name.capitalize()
    initial = name[0]
    new_user = {"Name": name, "Age": age, "Initial": initial}
    lib = pd.concat([lib,pd.DataFrame([new_user])], ignore_index=True)
    return {"message": f"User {name} added succesfully!"}    

# DELETE - delete by name
@app.delete("/delete/")
def delete_user(name: str):
    name = name.capitalize()
    if name in lib["Name"].values:
        lib.drop(lib[lib["Name"] == name].index, inplace=True)
        lib.reset_index(drop=True, inplace=True)
        return {"message": f"{name} removed successfully!"}
    return {"message": f"User {name} not found."}

# GET - show current added users
@app.get("/show/")
def show_list():
    global lib
    if(lib.empty):
        return {"message": "No users in the library."}
    else:
        return {"Users":lib.to_dict(orient="records")}

# POST - add users from .csv
@app.post("/add_csv/")
def add_user_from_csv(file: UploadFile = File(...)):
    global lib
    df = pd.read_csv(file.file)
    if "Name" not in df.columns or "Age" not in df.columns:
        return {"message": 'Please ensure the .csv file has "Name" and "Age" columns.'}

    df["Name"] = df["Name"].str.capitalize()
    df["Initial"] = df["Name"].str[0]
    df = df[["Name", "Age", "Initial"]]
    lib = pd.concat([lib, df], ignore_index = True)
    return {"message": f"{len(df)} users added to library."}


# GET - get average age according to initial group
@app.get("/avg/")
def get_average():
    global lib
    grouped = lib.sort_values(by="Initial")
    grouped = grouped.groupby("Initial")["Age"].mean()

    # grouped = lib.groupby("Initial")["Age"].mean().reset_index()
    # grouped = grouped.sort_values(by="Initial")
    # grouped.rename(columns={"Age": "Average age"}, inplace=True)

    res = grouped.to_dict()
    return res