from celery import Celery, Task


def make_celery(app):
    """
    Initialize and configure Celery within the Flask app context.
    """
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        task_cls=FlaskTask,
        include=['bot.commands.search_alumni']    # include the task module
    )
    celery_app.set_default()
    app.extensions['celery'] = celery_app
    return celery_app