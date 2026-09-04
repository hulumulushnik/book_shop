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
- GET /api/books/<id>/         (розширений BookDetailSerializer)
- GET /api/borrowings/
- /admin/                      (Django admin)
