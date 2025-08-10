from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()
    class Meta:
        model = MyUser
        fields = ('id','username','password','fullname','tokens')

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    def validate(self, data):
        #check password
        password = data.get("password")
        if len(password) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters")
        return data

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)