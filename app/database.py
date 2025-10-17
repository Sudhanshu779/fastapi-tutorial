from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if SessionLocal != None:
    print("Database connection was successful")

Base = declarative_base()


# Dependency for database
def get_db():
    db = SessionLocal()  # sessionlocal class is defined in database.py
    try:
        yield db
    finally:
        db.close()


# TO USE RAW SQL :

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="Sud@2001",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()  # used to excecute sql queries
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)  # retry after every 2 seconds
