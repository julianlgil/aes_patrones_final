FROM python:3.11-slim-buster

RUN apt-get update && apt-get -y install libpq-dev gcc

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
