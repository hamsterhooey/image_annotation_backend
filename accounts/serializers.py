from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "is_staff", "is_superuser")
