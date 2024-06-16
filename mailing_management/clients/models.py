from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    PERIODICITY_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField()
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Mailing {self.id} - {self.status}"


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    server_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Attempt {self.id} - {self.status}"
