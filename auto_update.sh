#!/bin/bash
cd /home/coimpre/tu_repo
git fetch origin
git reset --hard origin/main
touch /var/www/coimpre_pythonanywhere_com_wsgi.py
