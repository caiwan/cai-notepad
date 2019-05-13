# exec ./wait-for-it.sh -h database -p 5432 -t 240
# cat ./config/production.py
python manage.py bootstrap migrate admin admin
