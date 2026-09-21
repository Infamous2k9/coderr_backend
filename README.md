# Coderr Backend

A Django REST Framework backend for **Coderr**, a marketplace platform where
business users publish service offers with tiered pricing (basic/standard/
premium), and customer users can order and review them.

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- django-filter (offer search/filtering)
- django-cors-headers (frontend integration)
- django-environ (environment variable management)
- Pillow (image uploads)
- SQLite (development database)

## Setup

1. Clone the repository and navigate into the project folder.

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables (see below).

5. Create the database
   Migrations are not tracked in version control, so they are generated on first setup:

```bash
python manage.py makemigrations accounts offers orders reviews
python manage.py migrate
```

This creates db.sqlite3 in the project root.

6. Create a superuser (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

The API is now available at `http://127.0.0.1:8000/api/`.
The Django admin interface is available at `http://127.0.0.1:8000/admin/`.

## Environment Variables

Copy `.env.template` to `.env` and fill in your own values:

```bash
cp .env.template .env
```

| Variable               | Description                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `SECRET_KEY`           | Django's cryptographic signing key. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG`                | `True` for local development, `False` in production                                                                                                                |
| `ALLOWED_HOSTS`        | Comma-separated list of allowed hostnames                                                                                                                          |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed frontend origins (e.g. `http://127.0.0.1:5500` for a Live Server frontend)                                                         |

`.env` is git-ignored and must never be committed.

## Authentication

The API uses token-based authentication. After registering or logging in,
include the returned token in subsequent requests:

```
Authorization: Token <your-token>
```

## Main Endpoints

| Endpoint                                   | Description                          |
| ------------------------------------------ | ------------------------------------ |
| `POST /api/registration/`                  | Register a new user                  |
| `POST /api/login/`                         | Log in and receive an auth token     |
| `GET/PATCH /api/profile/{pk}/`             | Retrieve or update a user profile    |
| `GET /api/profiles/business/`              | List all business profiles           |
| `GET /api/profiles/customer/`              | List all customer profiles           |
| `GET/POST /api/offers/`                    | List or create offers                |
| `GET/PATCH/DELETE /api/offers/{id}/`       | Retrieve, update, or delete an offer |
| `GET /api/offerdetails/{id}/`              | Retrieve a single pricing tier       |
| `GET/POST /api/orders/`                    | List or create orders                |
| `PATCH/DELETE /api/orders/{id}/`           | Update status or delete an order     |
| `GET /api/order-count/{business_user_id}/` | Count of in-progress orders          |
| `GET /api/completed-order-count/{id}/`     | Count of completed orders            |
| `GET/POST /api/reviews/`                   | List or create reviews               |
| `PATCH/DELETE /api/reviews/{id}/`          | Update or delete a review            |
| `GET /api/base-info/`                      | Platform-wide statistics             |

## Notes & Special Behavior

- Registration requires a `type` field (`customer` or `business`); a matching
  `Profile` is created automatically.
- Only business users can create offers; only customer users can create
  orders and reviews.
- An offer must always contain exactly 3 details, one each of type `basic`,
  `standard`, and `premium`.
- A customer can leave only one review per business profile.
- Deleting an order is restricted to admin (staff) users.
- `GET /api/offers/` supports `creator_id`, `min_price`, `max_delivery_time`,
  `ordering` (`updated_at` or `min_price`), `search` (title/description),
  and `page_size` query parameters.
- Uploaded images (profile pictures, offer images) are served from `/media/`
  during development.
- CORS is configured via `CORS_ALLOWED_ORIGINS` in `.env` for a local
  frontend.
