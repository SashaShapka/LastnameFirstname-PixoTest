# Product Manager API

> **Note:** The Docker Compose file was not fully tested due to time constraints.
> PostgreSQL was used locally, Redis was containerized only.
> The database can be created using `create_db.ps1` (if `psql` is installed on Windows), and dropped using `drop_db.ps1`.
> Initial product data was populated using `insert_products.sql`.
> Unit tests were partially implemented due to time limits.
> Main start point is __main__.py

## ✨ Project Overview
This is a RESTful API service for managing products in an online store. It includes full CRUD operations,
user authorization, filtering capabilities, and basic statistics (e.g., most frequently added product).

### 📊 Features
- User authentication with JWT
- Role-based access control (admin vs user)
- CRUD operations on products (create, read, update, delete)
- Product filtering by name, price, and classification
- User-specific product selections
- Product popularity statistics
- Redis caching
- Rate limiting (per-user)

---

## 📄 Database Schema

### `products`
- `id` (UUID): primary key
- `name` (str): name of the product
- `description` (str): product description
- `price` (float): product price
- `in_stock` (int): available stock
- `classification` (str): one of `education`, `gaming`, or `home_goods`
- `created_at` (datetime): creation timestamp
- `updated_at` (datetime): last update timestamp

### `users`
- `id` (UUID): primary key
- `username` (str): unique
- `hashed_password` (str): password hash
- `role` (enum): `admin` or `user`
- `created_at` (datetime)
- `updated_at` (datetime)

### `user_product_requests`
- `id` (UUID): primary key
- `user_id` (UUID): FK to `users.id`
- `product_id` (UUID): FK to `products.id`
- `requested_at` (datetime): timestamp of selection
- Unique constraint: one user cannot add the same product more than once

---

## 🌐 Example API Usage

### 🔐 `POST /sign-up`
Returns JWT token.
```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

---

### 🔍 `GET /get_products`
Get all available products.
```json
[
  {
    "id": "...",
    "name": "Product 1",
    "description": "...",
    "price": 53.86,
    "in_stock": 47,
    "classification": "gaming",
    "created_at": "...",
    "updated_at": "..."
  }, ...
]
```

### 🔍 `GET /get_products_by_filter?price_max=424.83&classification=gaming`
Get filtered products.
```json
[
  {
    "id": "...",
    "name": "Product 1",
    "price": 53.86,
    "classification": "gaming"
  }, ...
]
```

### ➕ `POST /create_products`
Create a product.
```json
[
  {
    "name": "Book",
    "description": "English",
    "price": 150,
    "in_stock": 100,
    "classification": "education",
    "id": "...",
    "created_at": "...",
    "updated_at": "..."
  }
]
```

### ✏️ `PUT /update_products`
Update a product.
```json
[
  {
    "id": "...",
    "name": "Book",
    "price": 124,
    "in_stock": 20,
    "updated_at": "..."
  }
]
```

### ❌ `DELETE /delete_products`
Delete product(s).
```json
{
  "deleted_ids": ["..."],
  "message": "Products successfully deleted"
}
```

### 📊 `GET /statistic_product?values_on_the_top=1`
Top N most added products.
```json
[
  {
    "product_id": "...",
    "name": "book_1",
    "times_chosen": 3
  }
]
```

### ➕ `POST /chose_products`
Add product(s) to current user's selection.
```json
[
  {
    "id": "...",
    "name": "Product 6",
    "requested_at": "..."
  }
]
```

---

## 📖 Development
- Start point: `__main__.py`
- Runs: `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1`

---

## 🛋️ Docker
Only Redis is containerized. PostgreSQL was used locally.
```bash
docker-compose up --build
```

---

## ✅ Notes
- `.env` is required for Redis and configuration.
- Full test suite not implemented (time constraint).
- Alembic migrations can be used to track DB changes.

