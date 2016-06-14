web: gunicorn comfortbus.wsgi --log-file -
celery: python manage.py celery worker -B --loglevel=INFO --settings=comfortbus.settings.prod