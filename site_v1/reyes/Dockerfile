
FROM python:3.8-slim-bullseye

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

RUN pip install --upgrade cython
RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt