# Generated by Django 3.2.9 on 2021-11-28 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0007_alter_usercode_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercode',
            name='slug',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
