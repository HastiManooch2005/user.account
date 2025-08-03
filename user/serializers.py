from django_restframework import serializers
from user.models import *
from rest_framework_simplejwt.tokens import RefreshToken
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        #check password
        password = data['password']
        if len(password) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters")

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)