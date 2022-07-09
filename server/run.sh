#!/bin/bash
# source env file for eventual email config
#. env.sh
export FLASK_APP=run.py
export FLASK_DEBUG=1
export FLASK_ENV=development
#flask run --host=0.0.0.0 $1 $2 $3
flask run --port=8000 $1 $2 $3