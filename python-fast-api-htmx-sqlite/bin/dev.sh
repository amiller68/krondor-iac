#!/bin/bash

source venv/bin/activate

export HOST_NAME=http://localhost:9000
export LISTEN_ADDRESS=localhost
export LISTEN_PORT=9000
export DATABASE_PATH=:memory:
export DEBUG=True
export LOG_PATH=
python3 ./app/server.py

# Deactivate the virtual environment
deactivate

# Exit the script
exit 0
