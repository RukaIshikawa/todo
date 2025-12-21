import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from .models.task import Base

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

DB_URL = f"mysql+pymysql://{user}:{password}@{host}:3306/{database}?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()