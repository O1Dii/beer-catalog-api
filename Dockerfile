FROM python:3.8

ENV PYTHONBUFFERED 1
RUN mkdir /beer_catalog_api
WORKDIR /beer_catalog_api

COPY . /beer_catalog_api
RUN pip3 install pipenv
RUN pipenv install