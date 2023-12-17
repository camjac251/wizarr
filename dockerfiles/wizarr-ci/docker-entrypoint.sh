#!/bin/bash

cd /wizarr/backend

# Start Gunicorn processes
gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker --bind 0.0.0.0:5000 -m 007 run:app 2>&1 &

# Switch to non-root user before starting nginx
su -s /bin/bash wizarr -c '/usr/sbin/nginx -g "daemon off;"' 2>&1