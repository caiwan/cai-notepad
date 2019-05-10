#! /usr/bin/env sh
set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    source $PRE_START_PATH
else
    echo "There is no script $PRE_START_PATH"
fi

echo "env DATABASE $DATABASE"
echo "env DATABASE_NAME $DATABASE_NAME"
echo "env DATABASE_USER $DATABASE_USER"
echo "env DATABASE_PASSWORD $DATABASE_PASSWORD"
echo "env DATABASE_HOST $DATABASE_HOST"
echo "env DATABASE_PORT $DATABASE_PORT"
echo "env CSRF_SESSION_KEY $CSRF_SESSION_KEY"
echo "env GOOGLE_CLIENT_ID $GOOGLE_CLIENT_ID"
echo "env GOOGLE_CLIENT_SECRET $GOOGLE_CLIENT_SECRET"

cd /app
uwsgi --ini uwsgi.ini
