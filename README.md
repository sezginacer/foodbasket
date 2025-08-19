# FoodBasket - Delivery Hero Tech Hub Challenge Project

[![pipeline](https://github.com/sezginacer/foodbasket/actions/workflows/pipeline.yml/badge.svg)](https://github.com/sezginacer/foodbasket/actions/)
[![codecov](https://codecov.io/gh/sezginacer/foodbasket/branch/master/graph/badge.svg?token=L6LRM6TX8B)](https://codecov.io/gh/sezginacer/foodbasket)

A modern Django REST API for food delivery with real-time order processing, built with best practices and comprehensive features.

## 🚀 Features

- **Real-time Order Processing**: Redis-based PubSub system for live order status updates
- **Comprehensive API**: RESTful endpoints with automatic documentation
- **Security**: CORS support, rate limiting, and security headers
- **Performance**: Database indexing, caching, and query optimization
- **Monitoring**: Health checks, performance monitoring, and logging
- **Internationalization**: Turkish and English language support
- **Testing**: Comprehensive test suite with factory patterns
- **CI/CD**: Automated testing, linting, and deployment pipeline

## 🏗️ Architecture

### Core Components
- **Django 5.0.3**: Modern web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Primary database
- **Redis**: Caching and PubSub messaging
- **Docker**: Containerization

### Project Structure
```
foodbasket/
├── foodbasket/          # Main Django project
│   ├── common/         # Shared utilities and mixins
│   ├── orders/         # Order management
│   ├── products/       # Product catalog
│   ├── restaurants/    # Restaurant management
│   └── users/          # User management
├── pubsub/             # Real-time messaging system
├── demo/               # Demo scripts and services
└── scripts/            # Utility scripts
```

## 🛠️ Installation & Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.12+ (for local development)

### Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/sezginacer/foodbasket.git
   cd foodbasket
   ```

2. Start the application:
   ```bash
   docker-compose up
   ```

3. Access the application:
   - API: http://localhost:8080/api/v1/
   - Documentation: http://localhost:8080/api/docs/
   - Health Check: http://localhost:8080/health/

### Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://postgres:postgres@db:5432/foodbasket
REDIS_URL=redis://redis:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8080/api/docs/
- **ReDoc**: http://localhost:8080/api/redoc/
- **OpenAPI Schema**: http://localhost:8080/api/schema/

### Key Endpoints

#### Authentication
- `POST /users/register/` - User registration
- `POST /users/token/` - Get authentication token

#### Orders
- `GET /api/v1/orders/` - List orders (Admin only)
- `GET /api/v1/orders/{number}/` - Get order details
- `PATCH /api/v1/orders/{number}/` - Update order status
- `POST /orders/complete/` - Create new order
- `GET /api/v1/status/` - Order status statistics

#### Restaurants
- `GET /api/v1/restaurants/` - List restaurants
- `GET /restaurants/{uuid}/` - Restaurant details with products

#### Products
- `GET /api/v1/products/` - List products
- `GET /api/v1/categories/` - List categories

### Rate Limiting
- Registration/Token: 5 requests per minute
- Anonymous users: 100 requests per hour
- Authenticated users: 1000 requests per hour

## 🔄 Real-time Order Processing

The system uses a Redis-based PubSub system for real-time order processing:

### Order Workflow
1. **Order Created** → `WAITING_APPROVE`
2. **Approved** → `APPROVED`
3. **Preparing** → `PREPARING`
4. **On the Way** → `ON_THE_WAY`
5. **Delivered** → `DELIVERED`

### Demo Setup
1. Start the workers:
   ```bash
   docker-compose exec web sh
   cd demo
   python workers.py
   ```

2. In another terminal, start order generation:
   ```bash
   docker-compose exec web sh
   cd demo
   python order_populator.py
   ```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='./foodbasket' manage.py test
coverage report
```

### Test Structure
- Unit tests for models and services
- Integration tests for API endpoints
- Factory patterns for test data generation

## 📊 Monitoring & Health Checks

### Health Endpoints
- `GET /health/` - Basic health check
- `GET /status/system/` - Comprehensive system status

### Performance Monitoring
- Request/response logging
- Slow request detection (>1s)
- Processing time headers

### Logging
- Structured logging with different levels
- File and console output
- Request tracking

## 🔒 Security Features

- **CORS Protection**: Configurable cross-origin requests
- **Rate Limiting**: Prevents abuse and DDoS
- **Security Headers**: XSS protection, content type sniffing
- **Input Validation**: Comprehensive model validation
- **Authentication**: Token-based authentication

## 🚀 Performance Optimizations

### Database
- Strategic indexes on frequently queried fields
- Query optimization with select_related and prefetch_related
- Connection pooling

### Caching
- Redis-based caching for frequently accessed data
- Session storage in Redis
- Cache invalidation strategies

### API Optimization
- Pagination for large datasets
- Filtering and ordering capabilities
- Efficient serialization

## 🌍 Internationalization

The application supports multiple languages:
- **English** (en-us)
- **Turkish** (tr-tr)

Set the `Accept-Language` header in requests to get localized responses.

## 🔧 Development

### Code Quality
- **Black**: Code formatting
- **isort**: Import sorting
- **Type hints**: Comprehensive type annotations

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 📦 Deployment

### Docker Deployment
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Production Considerations
- Set `DEBUG=False`
- Configure proper `SECRET_KEY`
- Set up SSL/TLS certificates
- Configure production database
- Set up monitoring and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is part of the Delivery Hero Tech Hub Challenge.

## 🆘 Support

For questions or issues:
- Check the API documentation
- Review the test cases
- Open an issue on GitHub

---

**Note**: Passwords for all demo users are set to `12345`
