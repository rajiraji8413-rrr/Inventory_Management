
# Inventory Management System

## Project Overview

The Inventory Management System is a Django REST Framework-based application designed to manage products, categories, suppliers, purchases, sales, and stock levels.

It provides REST APIs to manage inventory operations and automatically updates product stock when purchases are received and sales are completed.

## Features

- Category Management
- Product Management
- Supplier Management
- Purchase Management
- Purchase Item Management
- Sales Management
- Sale Item Management
- Automatic Stock Updates
- Low Stock Detection
- Product Search and Filtering
- MySQL Database Integration
- Django REST Framework Browsable API

## Technologies Used

- Python
- Django
- Django REST Framework
- MySQL
- HTML
- CSS
- JavaScript
- REST API

## Project Structure

```text
Inventory_Management/
│
├── inventory/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── inventory_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Inventory_Management
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Add your own MySQL credentials:

```env
DB_NAME=inventory_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
DEBUG=True
```

### 6. Create MySQL Database

```sql
CREATE DATABASE inventory_db;
```

### 7. Run Migrations

```bash
python manage.py migrate
```

### 8. Start Development Server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/api/

## API Endpoints

| Module | Endpoint |
|---|---|
| API Root | `/api/` |
| Categories | `/api/categories/` |
| Products | `/api/products/` |
| Suppliers | `/api/suppliers/` |
| Purchases | `/api/purchases/` |
| Purchase Items | `/api/purchase-items/` |
| Sales | `/api/sales/` |
| Sale Items | `/api/sale-items/` |
| Low Stock | `/api/stock/low-stock/` |

## Stock Management Logic

### Purchase

When a purchase status changes from Pending to Received, the purchased quantity is automatically added to product stock.

### Sales

When a sale status changes from Pending to Completed, the sold quantity is automatically deducted from product stock.

### Low Stock

The Low Stock API identifies products whose available quantity is less than or equal to their minimum stock level.

## Testing

The following operations were tested successfully:

- Category, Product and Supplier APIs
- Purchase and Purchase Item APIs
- Sale and Sale Item APIs
- Purchase stock updates
- Sales stock deduction
- Low Stock API
- Django system checks and database migrations

## Author

Developed as a Django REST Framework learning project.
