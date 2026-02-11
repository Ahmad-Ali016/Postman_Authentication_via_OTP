from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class SignupSerializer(serializers.ModelSerializer):

    age = serializers.IntegerField(write_only=True)
    phone = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'phone', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove extra fields from validated_data before creating User
        age = validated_data.pop('age')
        phone = validated_data.pop('phone')
        validated_data.pop('confirm_password')

        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, age=age, phone=phone)
        return user