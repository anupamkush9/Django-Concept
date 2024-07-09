FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1

# for setting python output directly to the terminal with out buffering
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
COPY . /code/
