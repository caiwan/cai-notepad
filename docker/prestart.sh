#! /usr/bin/env sh

echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"

# ENTRYPOINT ["/app/wait-for-it.sh", "-t", "120", "postgresql", "--", "/app/entrypoint.sh"]

echo "
#! /usr/bin/env bash

# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head
"
