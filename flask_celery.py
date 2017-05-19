from celery import Celery

def make_celery(app):
    app.config.from_pyfile('config.py')
    celery = Celery(app.import_name, backend='CELERY_BACKEND',
                    broker='CELERY_BROKER_URL')
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
