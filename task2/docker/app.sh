#!/bin/bash

alembic upgrade head

cd src

python main.py