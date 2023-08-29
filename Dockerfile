FROM python:3.10-alpine3.16

COPY src /app
WORKDIR /app
EXPOSE 8000

RUN pip install -r requirements.txt

RUN adduser --disabled-password app-user

USER app-user
