FROM python:3.7.6-slim as default
LABEL maintainer="shirakiya"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV RUN_MODE "production"
ENV PORT "8000"
ENV MYSQL_USER "root"
ENV MYSQL_PASSWORD ""
ENV MYSQL_HOST "localhost"
ENV AWS_XRAY_DAEMON_ADDRESS "127.0.0.1:2000"
ENV API_TOKEN ""
ENV GOOGLE_API_KEY ""
ENV SLACK_URL ""
ENV TWITTER_CONSUMER_KEY ""
ENV TWITTER_CONSUMER_SECRET ""
ENV TWITTER_ACCESS_TOKEN ""
ENV TWITTER_ACCESS_TOKEN_SECRET ""
ENV ROLLBAR_ACCESS_TOKEN ""

COPY ./requirements.txt .
COPY ./requirements-deploy.txt .

RUN pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./manage.py .
COPY ./uwsgi.ini .
COPY ./jaaxman ./jaaxman
COPY ./app ./app

RUN mkdir -p /var/log/uwsgi

CMD ["/usr/local/bin/uwsgi", "--ini", "uwsgi.ini"]


FROM default as dev

ENV PYTHONUNBUFFERED 0
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements-dev.txt .

RUN pip install --no-cache-dir -r requirements-dev.txt
