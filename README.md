# FastAPI - Sample Management System

A comprehensive REST API for Sample Management built with FastAPI, featuring product management, inventory tracking, warehouse management, and transaction processing.

## 🚀 Features

- **Authentication & Authorization**: JWT-based authentication with refresh tokens
- **Product Management**: Create, read, update, and delete products
- **Bill of Materials (BOM)**: Manage product components and recipes
- **Material Management**: Track raw materials and supplies
- **Warehouse Management**: Multi-warehouse inventory tracking
- **Inventory Management**: Real-time inventory levels and stock tracking
- **Transaction Processing**: Purchase, sales, and transfer transactions
- **Category Management**: Organize products and materials by categories
- **Email Notifications**: Password reset and email verification
- **Background Tasks**: Celery integration for async operations
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Database Migrations**: Alembic for database schema management
- **Testing**: Comprehensive test suite with pytest

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL with SQLAlchemy ORM
- **Cache**: Redis
- **Task Queue**: Celery with Redis broker
- **Authentication**: JWT tokens
- **Email**: FastAPI-Mail
- **Documentation**: OpenAPI/Swagger
- **Testing**: pytest
- **Containerization**: Docker & Docker Compose
- **Database Migrations**: Alembic

## 📋 Prerequisites

- Python 3.13+
- Docker and Docker Compose
- MySQL 9.3+
- Redis 8.0+

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <https://github.com/haontuhcmut/reference-materials-fastapi.git>
   cd reference-materials-fastapi
   ```

2. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   DATABASE_URL="mysql+aiomysql://user:password@localhost:3306/inventory_db"
   TESTING_DATABASE_URL="mysql+aiomysql://user:password@localhost:3306/test_db"
   DOMAIN=""
   VERSION="api/v1"
   SECRET_KEY="your-secret-key"
   SALT="your-salt"
   ALGORITHM=""
   ACCESS_TOKEN_EXPIRE_MINUTES=
   JTI_EXPIRY_SECOND=
   REFRESH_TOKEN_EXPIRE_DAYS=
   MAIL_USERNAME="your-email@gmail.com"
   MAIL_PASSWORD="your-app-password"
   MAIL_FROM="your-email@gmail.com"
   MAIL_SERVER="smtp.gmail.com"
   BROKER_URL="redis://"
   BACKEND_URL="redis://"
   MYSQL_ROOT_PASSWORD="root-password"
   MYSQL_USER="user"
   MYSQL_PASSWORD="password"
   REDIS_URL="redis://"
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - API Documentation: http://domain:port/api/v1/docs
   - ReDoc Documentation: http://domain:port/api/v1/redoc
   - Celery Flower (Task Monitor): http://domain:port:5555

### Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   # Run database migrations
   alembic revision --autogeneration -m "init"
   alembic upgrade head
   ```

3. **Start the application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest test/test_auth.py
```

## 📁 Project Structure

```
ProductionInventoryManagement/
├── app/                          # Main application directory
│   ├── auth/                     # Authentication module
│   ├── bom/                      # Bill of Materials
│   ├── category/                 # Category management
│   ├── inventory/                # Inventory management
│   ├── material/                 # Material management
│   ├── product/                  # Product management
│   ├── pt_scheme/                # Product scheme management
│   ├── transaction/              # Transaction processing
│   ├── transaction_detail/       # Transaction details
│   ├── warehouse/                # Warehouse management
│   ├── db/                       # Database models and sessions
│   ├── utility/                  # Utility functions
│   ├── html_template/            # Email templates
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Configuration settings
│   ├── celery_task.py            # Celery task definitions
│   └── mail_config.py            # Email configuration
├── migration/                    # Database migrations
├── test/                         # Test files
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Docker image definition
├── requirements.txt              # Python dependencies
├── alembic.ini                   # Alembic configuration
└── README.md                     # This file
```

## 🐳 Docker Services

The application runs with the following services:

- **fastapi**: Main FastAPI application (Port 8000)
- **db**: MySQL database (Port 3306)
- **redis**: Redis cache and message broker (Port 6379)
- **celery-worker**: Background task worker
- **celery-flower**: Task monitoring interface (Port 5555)

## 📝 Database Migrations

To create and apply database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Hao Nguyen**
- GitHub: [@haontuhcmut](https://github.com/haontuhcmut)
- Email: nguyenminhhao1188@gmail.com

## 🆘 Support

If you encounter any issues or have questions, please:

1. Check the [API Documentation](http://domain:port/api/v1/docs)
2. Review the existing issues
3. Create a new issue with detailed information

---

**Note**: Make sure to update the environment variables and database credentials according to your setup before running the application.