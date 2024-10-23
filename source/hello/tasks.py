from hello.celery import app


@app.task
def print_text():
    print('Hello World')
