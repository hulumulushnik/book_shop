import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from library.models import Author, Book, Borrowing, Reader


class Command(BaseCommand):
    help = 'Populates the database with sample authors, books, readers and borrowings.'

    def handle(self, *args, **options):
        self.stdout.write('Populating library database...')

        # --- Authors -----------------------------------------------------
        authors_data = [
            {
                'name': 'Джордж Орвелл',
                'bio': 'Британський письменник і публіцист, автор антиутопій "1984" та "Колгосп тварин".',
                'birth_date': date(1903, 6, 25),
            },
            {
                'name': 'Джейн Остін',
                'bio': 'Англійська письменниця, класик світової літератури, авторка "Гордості та упередження".',
                'birth_date': date(1775, 12, 16),
            },
            {
                'name': 'Джордж Р. Р. Мартін',
                'bio': 'Американський письменник, автор циклу "Пісня льоду й полум\'я".',
                'birth_date': date(1948, 9, 20),
            },
            {
                'name': 'Агата Крісті',
                'bio': 'Британська письменниця, королева детективного жанру.',
                'birth_date': date(1890, 9, 15),
            },
            {
                'name': 'Дж. Р. Р. Толкін',
                'bio': 'Британський письменник і філолог, автор "Володаря перснів" та "Гобіта".',
                'birth_date': date(1892, 1, 3),
            },
        ]

        authors = []
        for data in authors_data:
            author, created = Author.objects.get_or_create(
                name=data['name'],
                defaults={'bio': data['bio'], 'birth_date': data['birth_date']},
            )
            authors.append(author)
        self.stdout.write(self.style.SUCCESS(f'  Authors ready: {len(authors)}'))

        # --- Books ---------------------------------------------------------
        books_data = [
            {'title': '1984', 'author': authors[0], 'pages': 328, 'isbn': '9780451524935', 'copies': 3},
            {'title': 'Колгосп тварин', 'author': authors[0], 'pages': 112, 'isbn': '9780451526342', 'copies': 2},
            {'title': 'Гордість і упередження', 'author': authors[1], 'pages': 279, 'isbn': '9780141439518', 'copies': 4},
            {'title': 'Емма', 'author': authors[1], 'pages': 474, 'isbn': '9780141439587', 'copies': 1},
            {'title': 'Гра престолів', 'author': authors[2], 'pages': 694, 'isbn': '9780553103540', 'copies': 5},
            {'title': 'Битва королів', 'author': authors[2], 'pages': 761, 'isbn': '9780553108033', 'copies': 0},
            {'title': 'Вбивство у "Східному експресі"', 'author': authors[3], 'pages': 256, 'isbn': '9780062693662', 'copies': 2},
            {'title': 'Десять негренят', 'author': authors[3], 'pages': 264, 'isbn': '9780062073488', 'copies': 3},
            {'title': 'Гобіт', 'author': authors[4], 'pages': 310, 'isbn': '9780547928227', 'copies': 6},
            {'title': 'Володар перснів', 'author': authors[4], 'pages': 1178, 'isbn': '9780618640157', 'copies': 0},
        ]

        books = []
        for data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=data['isbn'],
                defaults={
                    'title': data['title'],
                    'author': data['author'],
                    'description': f"Опис книги «{data['title']}».",
                    'published_date': date(2000, 1, 1) - timedelta(days=random.randint(0, 15000)),
                    'pages': data['pages'],
                    'available_copies': data['copies'],
                },
            )
            books.append(book)
        self.stdout.write(self.style.SUCCESS(f'  Books ready: {len(books)}'))

        # --- Readers ---------------------------------------------------------
        readers_data = [
            {'username': 'reader1', 'email': 'reader1@example.com'},
            {'username': 'reader2', 'email': 'reader2@example.com'},
            {'username': 'reader3', 'email': 'reader3@example.com'},
        ]

        readers = []
        for data in readers_data:
            reader, created = Reader.objects.get_or_create(
                username=data['username'],
                defaults={'email': data['email'], 'phone': '+380001112233'},
            )
            if created:
                reader.set_password('password123')
                reader.save()
            readers.append(reader)
        self.stdout.write(self.style.SUCCESS(f'  Readers ready: {len(readers)}'))

        # --- Borrowings ---------------------------------------------------------
        borrowings_plan = [
            {'book': books[0], 'reader': readers[0], 'returned': True, 'days_ago': 20, 'return_after': 10},
            {'book': books[2], 'reader': readers[0], 'returned': False, 'days_ago': 5},
            {'book': books[4], 'reader': readers[1], 'returned': True, 'days_ago': 30, 'return_after': 14},
            {'book': books[6], 'reader': readers[1], 'returned': False, 'days_ago': 2},
            {'book': books[8], 'reader': readers[2], 'returned': True, 'days_ago': 12, 'return_after': 7},
        ]

        created_count = 0
        for plan in borrowings_plan:
            borrowed_date = date.today() - timedelta(days=plan['days_ago'])
            return_date = None
            if plan['returned']:
                return_date = borrowed_date + timedelta(days=plan['return_after'])

            _, created = Borrowing.objects.get_or_create(
                book=plan['book'],
                reader=plan['reader'],
                defaults={
                    'return_date': return_date,
                    'is_returned': plan['returned'],
                },
            )
            if created:
                # borrowed_date has auto_now_add=True, so update it manually afterwards
                Borrowing.objects.filter(book=plan['book'], reader=plan['reader']).update(
                    borrowed_date=borrowed_date
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  Borrowings created: {created_count}'))
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
