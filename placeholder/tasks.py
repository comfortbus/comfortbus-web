import celery

@celery.task
def sum(a, b):
    return a + b