from typing import Optional
from sqlmodel import SQLModel, create_engine

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None



'''
echo=True.

It will make the engine print all the SQL statements it executes, which can help you understand what's happening.
'''
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

print('\x1b[6;30;42m' + 'Creating database...' + '\x1b[0m')

SQLModel.metadata.create_all(engine)

print('\x1b[6;30;42m' + 'Successfully created!' + '\x1b[0m')
