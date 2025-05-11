<h1 align="center">🚀 Dabas: Lightweight Database Management Library</h1>

<p align="center">
<a href="https://github.com/abbas-bachari/Dabas"><img src="https://img.shields.io/badge/Dabas%20-Version%201.0.0-green?style=plastic&logo=codemagic" alt="Dabas"></a>
<a href="https://github.com/abbas-bachari/Dabas"><img src="https://img.shields.io/badge/Python%20-3.7+-green?style=plastic&logo=Python" alt="Python"></a>
  <a href="https://pypi.org/project/Dabas/"><img src="https://img.shields.io/pypi/v/Dabas?style=plastic" alt="PyPI - Version"></a>
  <a href="https://pypi.org/project/Dabas/"><img src="https://img.shields.io/pypi/l/Dabas?style=plastic" alt="License"></a>
  <a href="https://pepy.tech/project/Dabas"><img src="https://pepy.tech/badge/Dabas?style=flat-plastic" alt="Downloads"></a>
</p>

## 🌟 **Introduction**

#### **Dabas** is a lightweight, easy-to-use library built on top of **SQLAlchemy** to simplify database operations in Python.  
#### It provides a streamlined interface for **connecting to databases**, **managing sessions**, and **performing CRUD operations** with minimal effort.

---

## ✨ **Features**

- 🔁 **Automatic Transaction Management** – Ensures safe commits and rollbacks.
- 🛠️ **Session Handling** – Provides a clean API for managing database sessions.
- 🔗 **Flexibility** – Supports multiple database engines via SQLAlchemy.
- ⚡ **Lightweight & Efficient** – Designed to be minimal while offering essential functionality.
- 🔍 **Advanced Filtering** – Supports OR/AND/range conditions.
- 📥 **Data Insertion** – Insert and bulk insert support.
- ✏️ **Data Modification** – Update and bulk update capabilities.
- 📄 **Easy Pagination** – Simplifies data navigation.
- 🛡️ **Safe Deletion** – Protects data with rollback support.
- 📦 **Consistent Output Handling** – Ensures structured data response.

---

## 📚 **Requirements**

- **Python 3.7+**
- **SQLAlchemy >= 1.4**

---

## 🔧 **Installation**

Install **Dabas** via **pip**:

```bash
pip install Dabas
```

## 💡 **Quick Start**

Here’s how you can **quickly set up and use Dabas** in your project.

```python
from Dabas import DatabaseManager, EngineFactory
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base
from time import time

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    time = Column(Integer, nullable=False)

    def __init__(self, order_id, product, price, time):
        self.order_id = order_id
        self.product = product
        self.price = price
        self.time = time

# Example data
order_1 = {"order_id": 1, "product": "product_1", "price": 100, "time": time()}
order_2 = Order(order_id=2, product="product_2", price=200, time=time())

# Database setup
engine = EngineFactory("data.db").sqlite()
db = DatabaseManager(engine=engine, base=Base)

# Create tables if they don't exist
db.create_tables()

# Insert records
db.insert(Order(**order_1))
db.insert(order_2)

# Query data
orders = db.get(Order, limit=2).to_json()
print(orders)
```

## 🖥️ **Expected Output**

```json
[
    {
        "order_id": 1,
        "price": 100.0,
        "product": "product_1",
        "time": 1746916053.5904622
    },
    {
        "order_id": 2,
        "price": 200.0,
        "product": "product_2",
        "time": 1746916053.5904622
    }
]
```

## **Advanced Examples with Dabas**

### 1️⃣ ***Bulk Insert Data Efficiently***

```python
# Insert multiple orders in one transaction
bulk_orders = [
    {"order_id": 3, "product": "product_3", "price": 150, "time": time()},
    {"order_id": 4, "product": "product_4", "price": 250, "time": time()},
    {"order_id": 5, "product": "product_5", "price": 350, "time": time()},
]

db.bulk_insert([Order(**order) for order in bulk_orders])
```

#### ✅ Faster insertion

#### ✅ Minimizes database overhead



### 2️⃣ ***Query with Filters (OR, AND, Range)***

```python
# Get orders where price is between 100 and 300
filtered_orders =  db.search(model_class,  range_filters={"price": (100, 200)}).to_json()



# Get orders with specific conditions (OR)
or_filtered_orders =db.search(model_class, or_conditions=[("product", "product_1"), ("price", 250)]).to_json()


# Get orders with specific conditions (AND)
and_filtered_orders =db.search(model_class, and_conditions=[("product", "product_4"), ("price", 250)]).to_json()


print(filtered_orders, or_filtered_orders, and_filtered_orders)
```

#### ✅ **Flexible filtering with OR/AND and range condition**


### 3️⃣ ***Update Records with Bulk Updat***

```python
# Update multiple records at once
update_data = [{"order_id": 3, "product": "Updated_Product_3"}, {"order_id": 4, "price": 275}]
db.bulk_update(Order, update_data)
```

#### ✅ **Easily update multiple records in one operation**

### 4️⃣ ***Safe Deletion with Rollback Suppor***

```python
# Delete an order safely
db.delete(Order, filters={"order_id":5})
```

#### ✅ **Ensures rollback support in case of errors**


### 5️⃣ ***Pagination for Large Dataset***

```python
# Get paginated results (2 items per page)
page_1 = db.paginate(page=1, per_page=2).to_json()
page_2 = db.paginate(page=2, per_page=2).to_json()

print(page_1, page_2)
```

#### ✅ **Easier navigation in large datasets**

---

### 🎯 Summary of New Features

#### ✅ Bulk insert for efficient data handling
#### ✅ Advanced filtering with OR/AND/Range conditions
#### ✅ Bulk updates for multiple records at once
#### ✅ Safe deletion with rollback protection
#### ✅ Pagination for large queries


## 📖 **Documentation**

For more details, visit the [official SQLAlchemy documentation](https://docs.sqlalchemy.org/).

## 📜 **License**

This project is licensed under the **MIT License**.

## 💖 **Sponsor** 

Support development by sponsoring on **[Github Sponsors](https://github.com/sponsors/abbas-bachari)**.
