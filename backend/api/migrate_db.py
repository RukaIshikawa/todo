import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

DB_URL = f"mysql+pymysql://{user}:{password}@{host}:3306/{database}?charset=utf8"
engine = create_engine(DB_URL, echo=True)
