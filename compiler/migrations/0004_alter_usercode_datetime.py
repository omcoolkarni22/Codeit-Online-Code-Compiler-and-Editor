# Generated by Django 3.2.9 on 2021-11-27 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0003_usercode_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercode',
            name='datetime',
            field=models.DateTimeField(),
        ),
    ]
