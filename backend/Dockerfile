FROM python:3.8-slim

WORKDIR /app_backend

COPY requirements.txt /app_backend

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app_backend
