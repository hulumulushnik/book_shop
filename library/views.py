from rest_framework import generics

from .models import Author, Book, Borrowing
from .serializers import (
    AuthorSerializer,
    BookDetailSerializer,
    BookSerializer,
    BorrowingSerializer,
)


class AuthorListCreateAPIView(generics.ListCreateAPIView):
    """GET: list all authors. POST: create a new author."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE a single author, looked up by `author_id`."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_url_kwarg = 'author_id'


class BookListCreateAPIView(generics.ListCreateAPIView):
    """GET: list all books. POST: create a new book."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE a single book."""

    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    """GET: list all borrowings. POST: register a new borrowing."""

    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


class AvailableBookListAPIView(generics.ListAPIView):
    """GET: list only the books that currently have available copies."""

    queryset = Book.objects.filter(available_copies__gt=0)
    serializer_class = BookSerializer
