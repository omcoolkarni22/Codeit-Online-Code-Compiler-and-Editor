from rest_framework import serializers
from .models import UserCode, ShareCode


class UserCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCode
        fields = ['name', 'datetime', 'slug', 'code', 'language']


class UserShareCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShareCode
        fields = ['code', 'language', 'permission', 'uniqueShareUrl']

