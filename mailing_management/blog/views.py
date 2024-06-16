from django.core.cache import cache
from django.core.cache.backends.base import InvalidCacheBackendError
from django.shortcuts import render

from clients.models import Mailing, Client
from .models import BlogPost


def home_view(request):
    try:
        mailings_count = cache.get('mailings_count')
        if mailings_count is None:
            mailings_count = Mailing.objects.count()
            cache.set('mailings_count', mailings_count, 60*15)

        active_mailings_count = cache.get('active_mailings_count')
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(status='started').count()
            cache.set('active_mailings_count', active_mailings_count, 60*15)

        unique_clients_count = cache.get('unique_clients_count')
        if unique_clients_count is None:
            unique_clients_count = Client.objects.values('email').distinct().count()
            cache.set('unique_clients_count', unique_clients_count, 60*15)

        random_blog_posts = BlogPost.objects.order_by('?')[:3]

    except InvalidCacheBackendError:
        # Если кэш недоступен, выполняйте действия без кэширования
        mailings_count = Mailing.objects.count()
        active_mailings_count = Mailing.objects.filter(status='started').count()
        unique_clients_count = Client.objects.values('email').distinct().count()
        random_blog_posts = BlogPost.objects.order_by('?')[:3]

    return render(request, 'home.html', {
        'mailings_count': mailings_count,
        'active_mailings_count': active_mailings_count,
        'unique_clients_count': unique_clients_count,
        'random_blog_posts': random_blog_posts,
    })


def about_view(request):
    return render(request, 'about.html')
