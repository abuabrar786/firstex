# E-Commerce Website Using Django

A professional but beginner-friendly Django college project with clean structure, improved UI, and a complete e-commerce flow.

## Key Features
- User Registration, Login, Logout using Django Authentication
- Product Catalog with Search + Category Filter
- Product image support using `image_url`
- Session-based Cart (add item, remove item, adjust quantity)
- Checkout and Order Placement
- Order History and Invoice-style Order Summary
- Admin panel setup for category, product, and orders

## Technology
- Django (latest stable in your environment)
- SQLite (default DB)
- Django Templates (MVT architecture)

## Project Structure
```
firstex/
├── manage.py
├── requirements.txt
├── ecommerce_site/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── shop/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
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

## Step-by-Step Setup
1. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run migrations**
   ```bash
   python manage.py migrate
   ```
4. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```
5. **Start development server**
   ```bash
   python manage.py runserver
   ```
6. **Open in browser**
   - Main app: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`

## Admin Data Entry Guide
- Create Categories first.
- Add Products and set:
  - Category
  - Name/Description
  - **Image URL** (recommended for good UI)
  - Price, Stock, Active status
