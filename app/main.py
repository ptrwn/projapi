from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select

from models import Projects

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/projects")
async def create_project(project: Projects):
    with Session(engine) as session:
        session.add(project)
        session.commit()
        session.refresh(project)
        return project



@app.get("/projects")
async def get_all_projects():
    with Session(engine) as session:
        projects = session.exec(select(Projects)).all()
        return projects


