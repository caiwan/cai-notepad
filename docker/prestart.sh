echo "Migrating / creating initial database"
python manage.py bootstrap migrate $DEFAULT_USER $DEFAULT_PASSWORD
