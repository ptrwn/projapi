from typing import Optional, List
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship



class UserRole(Enum):
    owner: str = "Owner"
    guest: str = "Guest"


class UsersProjects(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)
    user_role: UserRole = Field(default=UserRole.guest)
    users: "User" = Relationship(back_populates="project_links")
    projects: "Project" = Relationship(back_populates="user_links")

    
class UserBase(SQLModel):
    login: str = Field(default=None, unique=True)
    password: str = Field(default=None)
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_links: Optional[List["UsersProjects"]] = Relationship(back_populates="users")
class UserPost(UserBase): ...




class ProjectBase(SQLModel):
    name: str =  Field(default=None, unique=True)
    description: Optional[str] =  Field(default=None, unique=True)
class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # docs: Optional[List["Documents"]] = Relationship(back_populates="project")
    user_links: List["UsersProjects"] = Relationship(back_populates="projects")


class ProjectPost(ProjectBase):
    owner_id: int
    guests: Optional[List[int]]
    







# class Documents(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str =  Field(default=None, unique=True)
#     path: str = Field(default=None, unique=True)
#     project_id: int = Field(default=None, foreign_key="projects.id")
#     project: Projects = Relationship(back_populates="docs")





