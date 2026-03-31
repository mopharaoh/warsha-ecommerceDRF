FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirments.txt /app/

RUN pip install --default-timeout=100 --no-cache-dir -r requirments.txt

COPY . /app/