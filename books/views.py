from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework.response import Response
from books.serializer import UserSerializer, UserLoginSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


class UserSignUpViewSet(viewsets.ModelViewSet):
    """
    Creates the user
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        response = {}
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            response['token'] = token.key
            response['status'] = 'success'
            return Response(response, status=200)
        response['status'] = 'failed'
        return Response(response, status=401)