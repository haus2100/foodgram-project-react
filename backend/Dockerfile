FROM python:3.8-slim

RUN mkdir /app_backend

COPY requirements.txt /app_backend

RUN pip3 install -r /app_backend/requirements.txt --no-cache-dir

COPY ./ /app_backend

WORKDIR /app_backend
