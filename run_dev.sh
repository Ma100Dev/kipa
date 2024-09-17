#!/bin/bash
cd web
watchfiles \
    "python3 manage.py runserver --noreload" \
    .