#!/bin/bash
gunicorn --bind 0.0.0.0:5432 wsgi:app
