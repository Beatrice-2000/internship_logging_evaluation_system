#!/bin/bash
pip install -r requirements.txt
cd BACKEND
python manage.py migrate
python manage.py collectstatic --noinput