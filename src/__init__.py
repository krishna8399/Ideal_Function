# __init__.py
# Marks this directory as a Python package.

from sqlalchemy import create_engine
from database import Base

# Create SQLite engine
engine = create_engine("sqlite:///function_matching.db", echo=True)

# Create tables in the database
Base.metadata.create_all(engine)
