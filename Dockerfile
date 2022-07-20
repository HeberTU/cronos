FROM python:3.9-slim-buster

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

RUN mkdir -p /cronos


RUN mkdir -p /cronos/corelib
RUN mkdir -p /cronos/tests

COPY corelib /cronos/corelib
COPY tests /cronos/tests

WORKDIR /cronos