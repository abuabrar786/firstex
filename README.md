# E-Commerce Website Using Django

A beginner-friendly and professional Django project for an institute-level college project.

## Features
- User Registration & Login (Django Authentication)
- Product listing with category filter and search
- Add to cart / remove from cart
- Checkout and order placement
- Order history and order summary (invoice-style)
- Admin panel product and category management

## Tech Stack
- Django (latest stable supported by your environment)
- SQLite (default Django database)
- HTML templates with Django Template Language (DTL)

## Quick Start
1. Create virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Start server:
   ```bash
   python manage.py runserver
   ```
6. Open:
   - App: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`

## Project Structure
```
firstex/
├── manage.py
├── requirements.txt
├── ecommerce_site/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── shop/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       └── __init__.py
└── templates/
    ├── base.html
    ├── registration/
    │   ├── login.html
    │   └── register.html
    └── shop/
        ├── product_list.html
        ├── cart.html
        ├── checkout.html
        ├── order_history.html
        └── order_summary.html
```
