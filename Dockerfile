FROM python:3.6.3
LABEL maintainer="shirakiya"
LABEL version="1261a5743d4b7276b4d02a4fd11c8f3010a8c24c"

COPY ./requirements.txt /app/
COPY ./manage.py /app/
COPY ./app /app/app
COPY ./jaaxman /app/jaaxman

WORKDIR /app

RUN pip install -r requirements.txt
