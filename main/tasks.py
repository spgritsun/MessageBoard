import datetime

from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from MessageBoard.celery import app
from MessageBoard.settings import SITE_URL, DEFAULT_FROM_EMAIL
from main.models import Post, Category
from celery.schedules import crontab


@shared_task
def send_notification(user, email, comment_id, comment_text, com_post_id, com_post_author, comment_created=False):
    html_content = render_to_string(
        'comment_notification_email.html',
        {
            'user': user,
            'email': email,
            'comment_id': comment_id,
            'comment_text': comment_text,
            'com_post_id': com_post_id,
            'com_post_author': com_post_author,
            'comment_created': comment_created,

        }
    )
    msg = EmailMultiAlternatives(
        subject='Комментарий отправлен' if comment_created else 'Комментарий принят',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=email,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# @shared_task
# def send_daily_posts():
#     today = timezone.now()
#     last_week = today - datetime.timedelta(days=7)
#     posts = Post.objects.filter(post_time__gte=last_week)  # Берем все посты за последнюю неделю
#     categories = set(posts.values_list('categories__category_name', flat=True))  # Получаем все названия категорий
#     # этих постов
#     subscribers = set(
#         Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))  # Из
#     # объектов категорий постов извлекаем список email подписчиков на эти категории
#
#     html_content = render_to_string(
#         'daily_post.html',
#         {
#             'link': SITE_URL,
#             'posts': posts,
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject='Статьи за неделю',
#         body='',
#         from_email=DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# app.conf.beat_schedule = {
#     'action_every_monday_8am': {
#         'task': 'main.tasks.send_daily_posts',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday')
#     },
# }
