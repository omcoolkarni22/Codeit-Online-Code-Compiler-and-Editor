# Generated by Django 3.2.9 on 2021-11-27 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0005_usercode_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercode',
            name='slug',
        ),
    ]
