from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response

from books.models import BorrowedBook, Book
from books.serializer import UserSerializer, UserLoginSerializer, BorrowBooksSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


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
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {}
            username = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                response['token'] = token.key
                response['status'] = 'success'
                return Response(response, status=HTTP_200_OK)
            response['status'] = 'failed'
            return Response(response, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )


class BorrowBooksViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BorrowBooksSerializer
    queryset = BorrowedBook.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = BorrowedBook.objects.filter(user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = {}
        try:
            book = Book.objects.get(id=request.data.get('book_id'))
            if book.book_count < 1:
                response['status'] = 'Currently book is unavilable'
                return Response(response, status=HTTP_400_BAD_REQUEST)
            BorrowedBook.objects.create(book_id=request.data.get('book_id'),
                                        user=self.request.user, date=request.data.get('date'))
            book.book_count = book.book_count - 1
            book.save()
            response['status'] = 'success'
            return Response(response, status=HTTP_200_OK)
        except ObjectDoesNotExist:
            raise APIException("There is no book found")

