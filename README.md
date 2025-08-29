# fur-nest - Pet Adoption Platform API

fur-nest is a RESTful Pet Adoption Platform API built using Django REST Framework (DRF). It provides endpoints for managing pets, categories, adoptions, and adoption-histories. The project also implements JWT authentication using Djoser and includes API documentation with Swagger.

## Features
- Pet and category management
- Adoption functionality
- JWT authentication using Djoser
- API documentation using Swagger (drf_yasg)

## Technologies Used
- **Django** - Backend framework
- **Django REST Framework (DRF)** - API development
- **Djoser** - Authentication
- **Simple JWT** - JWT authentication
- **drf-yasg** - API documentation (Swagger)
- **PostgreSQL** (or SQLite) - Database

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tn592/fur-nest.git
   cd fur-nest
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```    |

## API Documentation
Swagger documentation is available at:
```
http://127.0.0.1:8000/swagger/
```

ReDoc documentation is available at:
```
http://127.0.0.1:8000/redoc/
```

## Environment Variables
Create a `.env` file in the root directory and add the following:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOSTS=*
EMIL_HOST=your_email_host
```

## License
This project is licensed under the MIT License.

---
### Author
[Tanzina](https://github.com/tn592)