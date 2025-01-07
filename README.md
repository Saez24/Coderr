# Coderr Backend

This is the backend for the Coderr application, developed with Django and the Django REST Framework.

## Prerequisites

- Python 3.x
- Django 3.x
- Django REST Framework

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Saez24
   cd coderr_backend
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**

   ```bash
   python manage.py makemigration
   python manage.py migrate
   ```

5. **For testing create guest Users and Superuser:**

   ```bash
   python manage.py create_users
   ```

6. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

   The application is available at `https://github.com/Saez24/Coderr_Frontend`

   The Backend will be accessible at `http://127.0.0.1:8000/admin`

   | Superuser | Username | Password |
   | --------- | -------- | -------- |
   | Admin     | admin    | admin123 |

   | Users         | Username | Password |
   | ------------- | -------- | -------- |
   | Customer-User | andrey   | asdasd   |
   | Business-User | kevin    | asdasd24 |

## Applications

The project consists of several Django applications:

- **base_info_app:** Management of basic information.
- **login_app:** Authentication and authorization.
- **offers_app:** Management of offers.
- **orders_app:** Management of orders.
- **profile_app:** User profiles.
- **registration_app:** User registration.
- **reviews_app:** Management of reviews.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure that all tests pass and that your code adheres to PEP8 standards.
