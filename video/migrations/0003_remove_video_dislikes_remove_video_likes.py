# Generated by Django 4.2.8 on 2023-12-16 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='video',
            name='likes',
        ),
    ]