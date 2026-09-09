import django_filters
from rest_framework import filters

from .models import Book, Borrowing


class BookFilter(django_filters.FilterSet):
    """
    FilterSet for Book with a variety of lookups:
      - title: iexact, icontains
      - author: exact (author id)
      - published_date: exact, year, year__gt, year__lt
      - pages: exact, lt, lte, gt, gte, range
      - available_copies: exact, gt
    """

    class Meta:
        model = Book
        fields = {
            'title': ['iexact', 'icontains'],
            'author': ['exact'],
            'published_date': ['exact', 'year', 'year__gt', 'year__lt'],
            'pages': ['exact', 'lt', 'lte', 'gt', 'gte', 'range'],
            'available_copies': ['exact', 'gt'],
        }


class BorrowingFilter(django_filters.FilterSet):
    """
    FilterSet for Borrowing, including filtering across related fields:
      - reader: exact (reader id), reader__username: icontains
      - book: exact (book id), book__title: icontains
      - borrowed_date: exact, year, month, year__gte
      - is_returned: exact
    """

    class Meta:
        model = Borrowing
        fields = {
            'reader': ['exact'],
            'reader__username': ['icontains'],
            'book': ['exact'],
            'book__title': ['icontains'],
            'borrowed_date': ['exact', 'year', 'month', 'year__gte'],
            'is_returned': ['exact'],
        }


class AvailableBooksFilterBackend(filters.BaseFilterBackend):
    """
    Custom filter backend: always restricts the queryset to books that
    currently have at least one available copy (available_copies > 0),
    regardless of any query parameters passed by the client.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(available_copies__gt=0)


class ActiveBorrowingsFilterBackend(filters.BaseFilterBackend):
    """
    Custom filter backend: always restricts the queryset to borrowings
    that have not been returned yet (is_returned=False).
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_returned=False)


class MinPagesFilterBackend(filters.BaseFilterBackend):
    """
    Custom filter backend driven by a raw query parameter (bonus task).
    Usage: GET /api/books/?min_pages=200
    Invalid (non-integer) values are silently ignored.
    """

    def filter_queryset(self, request, queryset, view):
        min_pages = request.query_params.get('min_pages')
        if min_pages:
            try:
                min_pages = int(min_pages)
                queryset = queryset.filter(pages__gte=min_pages)
            except ValueError:
                pass
        return queryset
