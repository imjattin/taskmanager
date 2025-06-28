from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False},
            "username": {"required": True, "allow_blank": False},
            "password": {
                "write_only": True,
                "min_length": 8,
                "style": {"input_type": "password"},
            },
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(AuthTokenSerializer):
    pass
