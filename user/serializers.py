from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

#Serializer to Get User Details using Django Token Authentication
class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["id", "first_name", "last_name", "username", "phone_number"]

#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=CustomUser.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = CustomUser
    fields = ('username', 'password', 'password2',
         'email', 'phone_number')
    extra_kwargs = {
      'username': {'required': True},
      'phone_number': {'required': True}
    }

  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  
  def create(self, validated_data):
    user = CustomUser.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      # first_name=validated_data['first_name'],
      # last_name=validated_data['last_name'],
      phone_number=validated_data['phone_number']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user


