# Generated by Django 3.2.9 on 2021-11-27 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0002_auto_20211126_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercode',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
