import os

from mongoengine import connect
from collections import *

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

SQL_DATABASE_URL = os.environ.get(os.environ.get("WHICH_DB_URL", "DATABASE_URL"))
SQL_HOST = os.environ.get("SQL_HOST")
SQL_PORT = os.environ.get("SQL_PORT")
SQL_DB_NAME = os.environ.get("SQL_DB_NAME")
SQL_DB_PASSWORD = os.environ.get("SQL_DB_PASSWORD")
SQL_USER_NAME = os.environ.get("SQL_USER_NAME")


MONGODB_HOST = os.environ.get("MONGODB_HOST")
MONGODB_PORT = os.environ.get("MONGODB_PORT")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME")
MONGODB_DB_PASSWORD = os.environ.get("MONGODB_DB_PASSWORD")
MONGODB_USER_NAME = os.environ.get("MONGODB_USER_NAME")

# SQL Connection String
if SQL_DATABASE_URL:
    SQL_DATABASE_URL = SQL_DATABASE_URL.replace("postgres://", "postgresql://")
else:
    SQL_DATABASE_URL = f"postgresql://{SQL_USER_NAME}:{SQL_DB_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB_NAME}"
    # DATABASE_URL=      postgres://ptcdisoiwaqexn:1415f9f2f3d7a32cc111ce58add8d0a6d010a5a2391693ade18afeb0618353c8@ec2-54-164-138-85.compute-1.amazonaws.com:5432/df7rns6jcliami

# MONGODB Connection String
MONGODB_DATABASE_URL = f"mongodb+srv://{MONGODB_USER_NAME}:{MONGODB_DB_PASSWORD}@{MONGODB_HOST}/{MONGODB_DB_NAME}"

engine = create_engine(SQL_DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

# NoSQL Connection
def initialize_mongodb():    
    connect(db=MONGODB_DB_NAME, host=MONGODB_DATABASE_URL)
    print("Connected to MongoDB")