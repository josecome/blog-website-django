# Generated by Django 4.1 on 2023-05-25 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_comments_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='user_id',
            new_name='user',
        ),
    ]
