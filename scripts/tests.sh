#!/bin/bash
#
# Run unit tests

source venv/Scripts/activate
export PYTHONPATH=src

if [ -z "$1" ]; then
    python -m unittest discover -v
else
    python -m unittest discover -v -p "*$1*.py"
fi