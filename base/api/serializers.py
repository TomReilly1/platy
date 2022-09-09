from rest_framework import serializers
from django.contrib.auth.models import User
from platy.models import Friends


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = '__all__'
