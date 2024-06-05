from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import PostCategory, Comment
from main.tasks import send_notification


@receiver(post_save, sender=Comment)
def notify_about_new_comment(created, instance, **kwargs):
    user = instance.user.username
    email = [instance.user.email]
    comment_id = instance.pk
    comment_text = instance.comment_text
    com_post_id = instance.post_id
    com_post_author = instance.post.author.user.username
    comment_created = True
    if created:
        send_notification.delay(user, email, comment_id, comment_text, com_post_id, com_post_author, comment_created)
    else:
        send_notification.delay(user, email, comment_id, comment_text, com_post_id, com_post_author)


