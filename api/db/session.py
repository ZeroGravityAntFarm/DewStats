from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os

db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_database = os.environ.get("DB_DATABASE")
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(db_username, db_password, db_host, db_port, db_database)

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    #Create database if it does not exist
    if not database_exists(engine.url):
        create_database(engine.url)

except Exception as e:
    print("Failed to connect to database.")
    print(e)
    exit()
    

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
