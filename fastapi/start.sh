#!/bin/bash

if [ "$1" == "freeze" ]; then
    echo "Freezing requirements.txt..."
    pip freeze > requirements.txt
    echo "requirements.txt generated."
else
    echo "Starting FastApi Server"
    fastapi dev main.py
fi

