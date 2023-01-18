
FROM python:3.9-slim-bullseye

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

# # for django
# RUN apk add --no-cache mariadb-connector-c-dev
# RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base
# RUN apk add netcat-openbsd

# # for numpy and pandas
# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev g++ \
#     libffi-dev openssl-dev \
#     libxml2 libxml2-dev \
#     libxslt libxslt-dev \
#     libjpeg-turbo-dev zlib-dev

RUN pip install --upgrade cython
RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt