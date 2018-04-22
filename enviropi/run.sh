#!/bin/bash
# 
if [ -f instance/instance.sh ]; then
    source instance/instance.sh
fi

gunicorn --bind 0.0.0.0:80 run
