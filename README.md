# 🗂️ Coder Backend

![Django](https://img.shields.io/badge/Django-4.x+-green.svg)
![REST API](https://img.shields.io/badge/REST-API-blue.svg)
![License](https://img.shields.io/github/license/Getinger96/KannMind_Backend)

> **A modern Freelancer plattform backend**, built with Django & Django REST Framework.  
> Provides a full-featured REST API for managing boards, lists (columns), and cards (tasks) — ideal for use with a separate frontend.

---

## 🚀 Features

- 🔐 User registration & authentication (Token/JWT/Session-based)
- 📋 Full CRUD operations for:
  - Profiles
  - Offers
  - Orders
  - Reviews
- 👥 Permission system for private/shared boards
- 🧩 RESTful API structure for frontend integration
- ⚙️ Admin panel available at `/admin/`

---

## ⚙️ Tech Stack

- 🐍 Python 3.x  
- 🧬 Django 4.x+  
- 🔌 Django REST Framework  
- 🗄️ SQLite / PostgreSQL (configurable)  
- 🔐 JWT Authentication (`djangorestframework-simplejwt` - optional)

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Getinger96/Coder_Backend
cd Coder_Backend
```

---

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate   
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Apply database migrations

```bash
python manage.py migrate
```

---


### 5️⃣ Create a superuser

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run the development server

```bash
python manage.py runserver
👉 API available at: http://127.0.0.1:8000/
👉 Admin panel under: http://127.0.0.1:8000/admin/
```

----

## 📖 API Overview

The API supports managing:

- 🧩 Profiles  
- 🗂️ Orders
- 🗂️ Offers
- 💬 Reviews   
- 👤 User authentication: Register & Login  

Use tools like Postman, Insomnia, or your frontend app to test and interact with the API.

---

## 🧪 Sample Endpoints

| Method | Endpoint                                | Description                            |
|--------|-----------------------------------------|----------------------------------------|
| POST   | `/api/registration/`                    | Register a new user                    |
| POST   | `/api/login/`                           | Log in a user                          |


### Profile
| Method | Endpoint                                | Description                            |
|--------|-----------------------------------------|----------------------------------------|
| GET    | `/api/profile/{profile_id}/`            | Retrieve a selected profile            |
| PATCH  | `/api/profile/{profile_id}/`            | Update some Data for youre profile     |
| GET    | `/api/profiles/business/`               | Retrieve profile with type business    |
| GET    | `/api/profiles/customer/`               | Retrieve profile with type customer    |


### Offers
| Method | Endpoint                                                | Description                            |
|--------|---------------------------------------------------------|----------------------------------------|
| GET    | `/api/offers`                                           | Get a list of Offers                   |
| POST   | `/api/offers/`                                          | Create an Offer                        |
| GET    | `/api/offers/{offer_id}`                                | Get an specific Offer                  |
| PATCH  | `/api/offers/{offer_id}/`                               | Update a specific Offer                |
| DELETE | `/api/offers/{offer_id}/`                               | Delete a specific Offer                |
| GET    | `/api/offerdetails/{offerdeatil_id}`                    | Get a specific offerdetail             |


### Orders
| Method | Endpoint                                                | Description                            |
|--------|---------------------------------------------------------|----------------------------------------|
| GET    | `/api/orders`                                           | Get a list of Orders                   |
| POST   | `/api/offers/`                                          | Create an Order                        |
| Patch  | `/api/orders/{order_id}`                                | Update a specific Order                |
| DELETE | `/api/orders/{order_id}/`                               | Delete a specific Order                |
| GET    | `/api/order-count/{business_user_id}/`                  | Get the number of actual order from a specific business_user|
| GET    | `/api/completed-order-count/{business_user_id}/`        | Get the number of completed orders from a specific business_user|

### Reviews
| Method | Endpoint                                                | Description                            |
|--------|---------------------------------------------------------|----------------------------------------|
| GET    | `/api/reviews`                                          | Get a list of Reviews                  |
| POST   | `/api/reviews/`                                         | Create an Review                       |
| PATCH  | `/api/reviews/{review_id}/`                             | Update a specific Review               |
| DELETE | `/api/reviews/{review_id}/`                             | Delete a specific Review               |




Full endpoint details are defined in your `urls.py` or browsable via the Django REST Framework interface.

---

## 📂 Project Structure (Quick Overview)

Coder_Backend/
├── coder/ # Core app
│ ├── models.py # Data models
│ ├── views.py # API views
│ ├── serializers.py # DRF serializers
│ └── urls.py # API routing
├── manage.py
├── requirements.txt

---

## 🤝 Contributing

Pull requests are welcome!  
If you find a bug or have a suggestion, feel free to open an issue.

---

## 📄 License

MIT License © Getinger96

---

## 📬 Contact

For questions or collaboration:  
📘 [LinkedIn](https://www.linkedin.com/in/erich-getinger-45536a255/)







