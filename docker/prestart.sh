echo "--- Migration START"
python manage.py bootstrap migrate $DEFAULT_USER $DEFAULT_PASSWORD
echo "--- Migration END"
