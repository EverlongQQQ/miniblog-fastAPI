from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.close()
        raise e  # Re-raise the exception to make FastAPI aware of it
    finally:
        db.close()

# connect to db 
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                             user='postgres', password='2006', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connection to DB was succesfull")
#         break
#     except Exception as error:
#         print("Connection not provided")
#         print("Error", error)
#         time.sleep(5)
