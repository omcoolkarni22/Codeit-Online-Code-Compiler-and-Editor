from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserCode)
admin.site.register(ShareCode)
admin.site.register(ForgetPassword)

