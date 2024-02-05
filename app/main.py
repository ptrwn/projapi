from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from models import User, ProjectPost

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


@app.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
    return user

@app.post("/users")
async def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.get("/users")
async def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

@app.post("/projects")
async def create_project(project: ProjectPost):
    print('===================================')
    print(project)

    # with Session(engine) as session:
    #     session.add(project)
    #     session.commit()
    #     session.refresh(project)
    #     return project