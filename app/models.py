from typing import Optional, List
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship


class Projects(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str =  Field(default=None, unique=True)
    description: Optional[str] =  Field(default=None, unique=True)
    docs: Optional[List["Documents"]] = Relationship(back_populates="project")
    user_links: Optional[List["UsersProjects"]] = Relationship(back_populates="project")

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str = Field(default=None, unique=True)
    password: str = Field(default=None)
    project_links: Optional[List["UsersProjects"]] = Relationship(back_populates="user")

class Documents(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str =  Field(default=None, unique=True)
    path: str = Field(default=None, unique=True)
    project_id: int = Field(default=None, foreign_key="projects.id")
    project: Projects = Relationship(back_populates="docs")


class UserRole(Enum):
    owner: str = "Owner"
    guest: str = "Guest"


class UsersProjects(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="projects.id", primary_key=True)
    user_role: UserRole = Field(default=UserRole.guest)
    user: "Users" = Relationship(back_populates="project_links")
    project: "Projects" = Relationship(back_populates="user_links")


'''

DB rough schema – user (login, hashed password), project (name, description), access between projects and user (user_id, project_id, access_type), documents (doc_id, path / s3 key, project_id) 

'''