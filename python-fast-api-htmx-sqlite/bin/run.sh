#!/bin/bash

source venv/bin/activate

export LISTEN_ADDRESS=0.0.0.0
export LISTEN_PORT=9000

export DEBUG=False
python3 ./app/server.py

# Deactivate the virtual environment
deactivate

# Exit the script
exit 0
