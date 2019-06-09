#! /usr/bin/env bash

set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ]; then
    echo "Running script $PRE_START_PATH"
    if [ "$DATABASE" == "sqlite" ]; then
      source $PRE_START_PATH
    else
#       exec ./wait-for-it.sh -h $DATABASE_HOST -p $DATABASE_PORT -t $DATABASE_WAIT_TIMEOUT -- echo "OK"
      while ! exec 6<>/dev/tcp/${DATABASE_HOST}/${DATABASE_PORT}; do
        echo "Trying to connect to DB ${DATABASE_HOST}"
        sleep 10
        echo "Retrying"
      done
      source $PRE_START_PATH
    fi
else
    echo "There is no script $PRE_START_PATH"
fi

echo "--- Starting supervisord"
exec /usr/bin/supervisord --configuration /etc/supervisord.conf
