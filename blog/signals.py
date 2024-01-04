from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from contents.models import (
    Post,
    Comment,
    Like,
    Share,
)


@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
   if created:
      print('New Post created:', instance.title)


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
   if created:
      print('New Comment created:', instance.comment)


@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
   if created:
      print('New Like added:', instance.tag)


@receiver(post_save, sender=Share)
def share_created(sender, instance, created, **kwargs):
   if created:
      print('New Share created:', instance.date_created)