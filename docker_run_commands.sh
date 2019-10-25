#!/usr/bin/env bash

pipenv run flask create_db
pipenv run flask load_data 4
pipenv run flask run