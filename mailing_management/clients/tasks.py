from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Mailing, MailingAttempt
from django.conf import settings


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', minutes=1)
    scheduler.start()


def send_mailing():
    now = timezone.now()
    mailings = Mailing.objects.filter(start_time__lte=now, status='created')

    for mailing in mailings:
        for client in mailing.clients.all():
            try:
                response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(mailing=mailing, status='success', server_response=response)
            except Exception as e:
                MailingAttempt.objects.create(mailing=mailing, status='failure', server_response=str(e))

        mailing.status = 'completed'
        mailing.save()
