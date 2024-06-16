from django import forms
from .models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'periodicity', 'status', 'message', 'clients']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
