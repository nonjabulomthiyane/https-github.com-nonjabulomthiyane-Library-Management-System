from django.shortcuts import render

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)

        if book.copies_available > 0:
            transaction = Transaction.objects.create(user=user, book=book)
            book.copies_available -= 1
            book.save()
            return Response({'status': 'Book checked out'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        user = request.user
        transaction_id = request.data.get('transaction_id')
        transaction = Transaction.objects.get(id=transaction_id)

        transaction.return_date = timezone.now()
        transaction.save()

        book = transaction.book
        book.copies_available += 1
        book.save()
        return Response({'status': 'Book returned'}, status=status.HTTP_200_OK)
