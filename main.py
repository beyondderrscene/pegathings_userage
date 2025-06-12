from fastapi import FastAPI, UploadFile, File, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pandas as pd

from models import User
from database import SessionLocal, engine, Base

app = FastAPI()

# ini basically CREATE TABLE IF NOT EXISTS users
Base.metadata.create_all(bind=engine)

#soalny tiap request mesti akses ke db kan, jdi ini function buat mrk bisa dpt session sendiri, trus ditutup 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Hello!"}


# POST - add user and age
@app.post("/add/")
def add_user(name: str, age: int, db: Session = Depends(get_db)):
    name = name.capitalize()
    initial = name[0]
    # basically create a new entry gitu, buat di append ke sql table nya
    # ini eqv nya INSERT INTO users (name, age, initial) VALUES ('Alice', 30, 'A');
    new_user = User(name=name, age=age, initial=initial)
    db.add(new_user)
    # ini kyk git push gitu, supaya bnrn dbnya ke modify
    db.commit()
    return {"message": f"User {name} added successfully!"}


# DELETE - delete by name
@app.delete("/delete/")
def delete_user(name: str, db: Session = Depends(get_db)):
    name = name.capitalize()
    # ini eqv nya SELECT * FROM users WHERE name = 'name' LIMIT 1 <- ini karena kita pake first()
    user = db.query(User).filter(User.name == name).first()
    if user:
        # trus ini ya lgsg delete
        # basically DELETE FROM users WHERE id = 'id'
        db.delete(user)
        db.commit()
        return {"message": f"{name} removed successfully!"}
    return {"message": f"User {name} not found."}


# GET - show current users
@app.get("/show/")
def show_list(db: Session = Depends(get_db)):
    # ini basically yg plg gampng, SELECT * FROM users
    users = db.query(User).all()
    if not users:
        return {"message": "No users in the library."}
    return {"Users": [{"Name": u.name, "Age": u.age, "Initial": u.initial} for u in users]}


# POST - add users from .csv
@app.post("/add_csv/")
def add_user_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    if "Name" not in df.columns or "Age" not in df.columns:
        return {"message": 'Please ensure the .csv file has "Name" and "Age" columns.'}

    df["Name"] = df["Name"].str.capitalize()
    df["Initial"] = df["Name"].str[0]
    count = 0
    for _, row in df.iterrows():
        user = User(name=row["Name"], age=int(row["Age"]), initial=row["Initial"])
        db.add(user)
        count += 1
    db.commit()
    return {"message": f"{count} users added to library."}


# GET - average age per initial
@app.get("/avg/")
def get_average(db: Session = Depends(get_db)):
    from sqlalchemy import func

    if db.query(User).count() == 0:
        return {"message": "No users registered."}    

    result = db.query(User.initial, func.avg(User.age)).group_by(User.initial).order_by(User.initial).all()
    return {initial: round(avg, 2) for initial, avg in result}
