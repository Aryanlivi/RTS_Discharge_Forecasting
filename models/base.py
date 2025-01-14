from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection URL
DATABASE_URL = f"postgresql://{os.getenv('username')}:{os.getenv('password')}@{os.getenv('server')}/{os.getenv('database')}"

# SQLAlchemy base and engine
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)

# Session maker
SessionLocal = sessionmaker(bind=engine)

