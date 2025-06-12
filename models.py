# disini kita define mau gimana bentuk database kita

from sqlalchemy import Column, Integer, String
from database import Base

# bikin table, ini eqv sama CREATE TABLE users
# pake (Base) soalny kt pake sqlalchemy, jadi minta dia yg bikinin kita mau gini
class User(Base):
    __tablename__ = "users"
    # skrg masuk ke column2nya
    # primary key ini kyk unique id mereka, dan ini bakal increment trs, ini diindex buat ngelookup
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    initial = Column(String, index=True)