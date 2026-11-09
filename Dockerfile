FROM python:3.13

RUN pip install fastapi[standard]

WORKDIR /app/src

