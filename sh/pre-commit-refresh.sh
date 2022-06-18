#!/usr/bin/env bash

pipenv run pre-commit clean && pipenv run pre-commit install --hook-type pre-commit --hook-type pre-push
