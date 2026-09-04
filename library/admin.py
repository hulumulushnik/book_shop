from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Author, Book, Borrowing, Reader


@admin.register(Reader)
class ReaderAdmin(UserAdmin):
    """Admin for the custom Reader (user) model."""

    fieldsets = UserAdmin.fieldsets + (
        ('Library info', {'fields': ('phone', 'address', 'registration_date')}),
    )
    readonly_fields = UserAdmin.readonly_fields + ('registration_date',)
    list_display = ('username', 'email', 'phone', 'registration_date', 'is_staff')
    search_fields = ('username', 'email', 'phone')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'book_count')
    search_fields = ('name',)
    list_filter = ('birth_date',)

    @admin.display(description='Number of books')
    def book_count(self, obj):
        return obj.book_count


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available_copies', 'is_available')
    search_fields = ('title', 'isbn', 'author__name')
    list_filter = ('author', 'published_date')

    @admin.display(boolean=True, description='Available')
    def is_available(self, obj):
        return obj.is_available


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'borrowed_date', 'return_date', 'is_returned')
    list_filter = ('is_returned', 'borrowed_date')
    search_fields = ('book__title', 'reader__username')
