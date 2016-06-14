web: gunicorn comfortbus.wsgi --log-file -
celery: python manage.py celery worker --loglevel=INFO --settings=comfortbus.settings.prod