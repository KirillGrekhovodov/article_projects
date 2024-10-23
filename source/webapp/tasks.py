from celery import shared_task


@shared_task()
def periodic_task():
    print('Periodic task')



@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 10})
def send_email_task(self, user_id, context: dict):
    # user = User.objects.get(pk=user_id)
    print('Sending email !!!!!!!!!!!!!!!')