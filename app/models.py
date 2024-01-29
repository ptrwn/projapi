from typing import Optional
from sqlmodel import Field, SQLModel


class Projects(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] =  Field(default=None, unique=True)