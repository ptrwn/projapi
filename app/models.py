from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class UserRole(Enum):
    owner: str = "Owner"
    guest: str = "Guest"


class UsersProjects(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    project_id: Optional[int] = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    user_role: UserRole = Field(default=UserRole.guest)
    users: "User" = Relationship(back_populates="project_links")
    projects: "Project" = Relationship(back_populates="user_links")


class UserBase(SQLModel):
    login: str = Field(default=None, unique=True)
    password: str = Field(default=None)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_links: Optional[List["UsersProjects"]] = Relationship(
        back_populates="users"
    )


class UserPost(UserBase): ...


class ProjectBase(SQLModel):
    name: str = Field(default=None, unique=True)
    description: Optional[str] = Field(default=None, unique=True)


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    docs: Optional[List["Document"]] = Relationship(back_populates="project")
    user_links: List["UsersProjects"] = Relationship(back_populates="projects")


class ProjectPost(ProjectBase):
    owner_id: int
    guests: Optional[List[int]]


class DocumentBase(SQLModel):
    name: str = Field(default=None, unique=True)
    path: str = Field(default=None, unique=True)


class Document(DocumentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(default=None, foreign_key="project.id")
    project: Project = Relationship(back_populates="docs")
