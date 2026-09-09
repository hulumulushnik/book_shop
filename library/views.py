from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import (
    ActiveBorrowingsFilterBackend,
    AvailableBooksFilterBackend,
    BookFilter,
    BorrowingFilter,
    MinPagesFilterBackend,
)
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
    """
    GET: list all books.

    Supports filtering via BookFilter:
      ?title__icontains=...   ?title__iexact=...
      ?author=<id>
      ?published_date=YYYY-MM-DD  ?published_date__year=YYYY
      ?published_date__year__gt=YYYY  ?published_date__year__lt=YYYY
      ?pages=...  ?pages__lt=...  ?pages__lte=...
      ?pages__gt=...  ?pages__gte=...  ?pages__range=100,300
      ?available_copies=...  ?available_copies__gt=0

    Plus a custom query parameter (bonus): ?min_pages=200

    POST: create a new book.
    """

    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [DjangoFilterBackend, MinPagesFilterBackend]


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE a single book."""

    queryset = Book.objects.select_related('author')
    serializer_class = BookDetailSerializer


class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: list all borrowings.

    Supports filtering via BorrowingFilter:
      ?reader=<id>  ?reader__username__icontains=...
      ?book=<id>    ?book__title__icontains=...
      ?borrowed_date=YYYY-MM-DD  ?borrowed_date__year=YYYY
      ?borrowed_date__month=MM   ?borrowed_date__year__gte=YYYY
      ?is_returned=true|false

    POST: register a new borrowing.
    """

    queryset = Borrowing.objects.select_related('book', 'reader')
    serializer_class = BorrowingSerializer
    filterset_class = BorrowingFilter


class AvailableBookListAPIView(generics.ListAPIView):
    """
    GET: list only the books that currently have available copies.

    Always applies AvailableBooksFilterBackend (available_copies > 0),
    on top of the regular BookFilter query-parameter filtering.
    """

    queryset = Book.objects.select_related('author').order_by('pk')
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [DjangoFilterBackend, AvailableBooksFilterBackend]


class ActiveBorrowingsAPIView(generics.ListAPIView):
    """
    GET: list only borrowings that have not been returned yet.

    Always applies ActiveBorrowingsFilterBackend (is_returned=False),
    on top of the regular BorrowingFilter query-parameter filtering.
    """

    queryset = Borrowing.objects.select_related('book', 'reader').order_by('-borrowed_date')
    serializer_class = BorrowingSerializer
    filterset_class = BorrowingFilter
    filter_backends = [DjangoFilterBackend, ActiveBorrowingsFilterBackend]
