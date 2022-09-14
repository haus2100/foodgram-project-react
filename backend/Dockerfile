FROM python:3.8-slim

WORKDIR /app/app_backend

COPY ./ /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ /app_backend
