from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserStatus, Promotion

User = get_user_model()

# CRUD User :

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'status', 'promotion']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        status = data.get('status')
        promotion = data.get('promotion')

        if status != UserStatus.STUDENT.value and promotion:
            data['promotion'] = None

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'status', 'promotion']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'status', 'promotion']

class UserDetailForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'status', 'promotion']
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'promotion']

# CRUD Promotion :

class PromotionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["name"]

class PromotionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["id", "name"]
        
class PromotionDetailSerializer(serializers.ModelSerializer):
    users = UserListSerializer(source='users_s_promotion', many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = ["id", "name", "users"]
                
class PromotionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["name"]

# Token :

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['email'] = user.email
        token['status'] = user.status
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
