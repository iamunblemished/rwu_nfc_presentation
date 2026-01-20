#!/bin/bash
cd /home/nfc/nfc_project
source env/bin/activate
python bridge_sensor.py &
python manage.py runserver 0.0.0.0:8000
