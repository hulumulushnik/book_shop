# Library API (Django REST Framework)

## Запуск проекту

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py populate_library   # заповнює БД тестовими даними
python manage.py createsuperuser    # опційно, для входу в /admin/
python manage.py runserver
```

## Endpoints

- GET /api/authors/
- GET /api/authors/<id>/
- GET /api/books/
- GET /api/books/available/
- GET /api/books/<id>/ (розширений BookDetailSerializer)
- GET /api/borrowings/
- GET /api/borrowings/active/
- /admin/ (Django admin)

## Filtering

Фільтрація реалізована через `django-filter` (`library/filters.py`).

### BookFilter (`/api/books/`, `/api/books/available/`)

| Query-параметр | Опис |
|---|---|
| `?title__iexact=Емма` | точна назва (без урахування регістру) |
| `?title__icontains=емма` | назва містить підрядок |
| `?author=1` | книги конкретного автора (по id) |
| `?published_date=1980-01-19` | точна дата видання |
| `?published_date__year=1980` | рік видання |
| `?published_date__year__gt=1950` | видано після 1950 року |
| `?published_date__year__lt=1950` | видано до 1950 року |
| `?pages=279` / `?pages__lt=300` / `?pages__lte=300` / `?pages__gt=300` / `?pages__gte=300` | кількість сторінок |
| `?pages__range=100,300` | діапазон сторінок |
| `?available_copies=0` / `?available_copies__gt=0` | кількість доступних примірників |
| `?min_pages=200` (бонус, custom backend) | мінімум 200 сторінок |

Приклад: `GET /api/books/?pages__range=100,300&available_copies__gt=0`

> ⚠️ БД — SQLite. `icontains`/`iexact` для кирилиці на SQLite регістронезалежні лише
> в межах ASCII (відома особливість SQLite), тому для кириличних назв варто
> вказувати запит із тим самим регістром, що й у базі, або використовувати
> `icontains` з першою літерою у правильному регістрі.

### BorrowingFilter (`/api/borrowings/`, `/api/borrowings/active/`)

| Query-параметр | Опис |
|---|---|
| `?reader=1` | позики конкретного читача (по id) |
| `?reader__username__icontains=john` | пошук по імені користувача читача |
| `?book=1` | позики конкретної книги (по id) |
| `?book__title__icontains=гобіт` | пошук по назві книги |
| `?borrowed_date=2026-08-31` | точна дата позики |
| `?borrowed_date__year=2026` | рік позики |
| `?borrowed_date__month=8` | місяць позики |
| `?borrowed_date__year__gte=2025` | позики починаючи з 2025 року |
| `?is_returned=false` / `?is_returned=true` | повернуто / не повернуто |

Приклад: `GET /api/borrowings/?is_returned=false&borrowed_date__year=2026`

### Custom Filter Backends

- **`AvailableBooksFilterBackend`** — завжди застосовується на
  `GET /api/books/available/`, обмежуючи вибірку книгами з
  `available_copies > 0` (незалежно від параметрів запиту).
- **`ActiveBorrowingsFilterBackend`** — завжди застосовується на
  `GET /api/borrowings/active/`, обмежуючи вибірку позиками з
  `is_returned=False`.
- **`MinPagesFilterBackend`** (бонус) — читає `?min_pages=N` вручну з
  `request.query_params` і додає `pages__gte=N`; невалідні значення
  ігноруються. Підключений до `GET /api/books/`.

# book_shop
