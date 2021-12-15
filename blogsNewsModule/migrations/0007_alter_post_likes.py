# Generated by Django 3.2.9 on 2021-12-15 01:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogsNewsModule', '0006_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='blog_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]