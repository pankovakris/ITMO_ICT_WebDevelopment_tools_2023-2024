FROM python:3.12-slim

WORKDIR /parser
COPY /requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache -r requirements.txt

COPY task1.py .
