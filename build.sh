#!/bin/bash
# build.sh

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
flask db upgrade

echo "Collecting static files..."
flask collectstatic --noinput 
