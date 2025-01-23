#!/bin/bash

# Print Python path for debugging
echo "PYTHONPATH: $PYTHONPATH"

# Print directory contents for debugging
echo "App directory contents:"
ls -R /app

# Run gunicorn with verbose logging
exec gunicorn \
    --chdir /app \
    --bind 0.0.0.0:8050 \
    --log-level debug \
    --pythonpath /app \
    beta.python.No.1.main:server
