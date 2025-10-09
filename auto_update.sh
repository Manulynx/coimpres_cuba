#!/bin/bash
cd /home/Coimpre/coimpres_cuba
git fetch origin
git reset --hard origin/main
touch /var/www/coimpre_pythonanywhere_com_wsgi.py
