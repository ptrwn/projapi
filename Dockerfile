FROM python:3.11

RUN pip install fastapi uvicorn sqlmodel
WORKDIR /app

COPY /app .

ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
