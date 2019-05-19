#! /usr/bin/env sh

set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ]; then
    echo "Running script $PRE_START_PATH"
    if [ "$DATABASE" == "sqlite" ]; then
      source $PRE_START_PATH
    else
      exec ./wait-for-it.sh -h $DATABASE_HOST -p $DATABASE_PORT -t $DATABASE_WAIT_TIMEOUT -- $PRE_START_PATH
    fi
else
    echo "There is no script $PRE_START_PATH"
fi

if [ "$DATABASE" == "sqlite" ]; then
  exec $@
else
  exec ./wait-for-it.sh -h $DATABASE -p $DATABASE_PORT -t $DATABASE_WAIT_TIMEOUT -- $@
fi
