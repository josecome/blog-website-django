# Generated by Django 4.1 on 2023-11-22 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contents', '0005_alter_shares_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=20)),
                ('object_id', models.PositiveIntegerField()),
                ('created_date', models.DateField(null=True)),
                ('updated_date', models.DateField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
        migrations.RenameModel(
            old_name='Shares',
            new_name='Share',
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
        migrations.AddIndex(
            model_name='like',
            index=models.Index(fields=['content_type', 'object_id'], name='contents_li_content_f14242_idx'),
        ),
    ]