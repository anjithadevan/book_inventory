from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from books.models import BorrowedBook, Book


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        required=False
    )
    last_name = serializers.CharField(
        required=False
    )
    password = serializers.CharField(required=True, min_length=8)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'username')


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(label='Email', write_only=True)
    password = serializers.CharField(label='Password', write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class BorrowBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ('book_id', 'date')
