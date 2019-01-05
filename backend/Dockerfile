FROM python:3.6.2
LABEL maintainer="shirakiya"

ENV PYTHONUNBUFFERED "0"
ENV RUN_MODE "production"
ENV PORT "8000"
ENV MYSQL_USER "root"
ENV MYSQL_PASSWORD ""
ENV MYSQL_HOST "localhost"
ENV API_TOKEN ""
ENV GOOGLE_API_KEY ""
ENV SLACK_URL ""
ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""
ENV AWS_XRAY_DAEMON_ADDRESS "127.0.0.1:2000"

COPY ./requirements.txt /app/
COPY ./manage.py /app/
COPY ./app /app/app
COPY ./jaaxman /app/jaaxman

WORKDIR /app

RUN pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:$PORT"]
