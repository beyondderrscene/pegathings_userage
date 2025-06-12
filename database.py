# jadi file ini buat ngedefine mau connect gimana ke databasenya

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mydb"
# postgresql:// -> pake postgresql
# postgres:postgres -> username:pwd
# @localhost:5432 -> connect ke port mana
# /mydb -> database gw buat nyimpen file

# buat bikin engine -> main connection tool ke databasenya
engine = create_engine(DATABASE_URL)
# buat bikin session ini kaya temp connection ke database, soalny kt cmn pake buat fastapi ini
# ini buat add delete ask for data blablabla
SessionLocal = sessionmaker(bind=engine)
# basically template buat semua data
Base = declarative_base()