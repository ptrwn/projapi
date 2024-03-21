from contextlib import asynccontextmanager

from fastapi import FastAPI
from models import Project, ProjectPost, User, UserPost, UserRole, UsersProjects
from sqlmodel import Session, SQLModel, create_engine, select

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
async def create_user(user: UserPost):
    user = User(login=user.login, password=user.password)
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
    with Session(engine) as session:
        owner = session.get(User, project.owner_id)
        new_project = Project(name=project.name, description=project.description)
        owner_project = UsersProjects(
            users=owner, projects=new_project, user_role=UserRole.owner
        )
        session.add(owner)
        session.add(new_project)
        session.add(owner_project)
        session.commit()

        if project.guests:
            guests = [session.get(User, guest) for guest in project.guests]
            guests_project = [
                UsersProjects(
                    users=guest, projects=new_project, user_role=UserRole.guest
                )
                for guest in guests
            ]

            for guest, guest_proj in zip(guests, guests_project):
                session.add(guest)
                session.add(guest_proj)
            session.commit()


@app.put("/project/{project_id}")
async def update_project(project_id): ...


@app.get("/project/{project_id}")
async def get_project(project_id): ...


@app.get("/projects/{user_id}")
async def get_projects_for_user(user_id):
    res = []

    with Session(engine) as session:
        user = session.get(User, user_id)
        for proj_link in user.project_links:
            role = proj_link.user_role.value
            project = session.get(Project, proj_link.project_id)
            res.append(
                {
                    "role": role,
                    "project_name": project.name,
                    "project_desription": project.description,
                }
            )

    return res
