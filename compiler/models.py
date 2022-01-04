from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Model for saving user codes
class UserCode(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, blank=True)
    code = models.TextField(default='', null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=150, null=True, unique=True, blank=True)

    def __str__(self):
        return self.user.username


# model for sharing code
class ShareCode(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    code = models.TextField(default='', null=True, blank=True)
    language = models.CharField(max_length=15, null=True, blank=True)
    permission = models.CharField(max_length=150, null=True, blank=True)
    uniqueShareUrl = models.CharField(max_length=150, null=True, unique=True, blank=True)

    def __str__(self):
        return self.user.username


# model for forget password link saving
class ForgetPassword(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    link = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.user.username

