# Generated by Django 4.0.5 on 2022-06-15 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
