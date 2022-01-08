# Generated by Django 3.2.9 on 2021-11-28 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compiler', '0008_usercode_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercode',
            name='slug',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='ShareCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(blank=True, default='', null=True)),
                ('language', models.CharField(blank=True, max_length=15, null=True)),
                ('permission', models.CharField(blank=True, max_length=150, null=True)),
                ('slug', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]