# Quant API - Bitcoin Analysis Platform

A comprehensive ORM-based API built with FastAPI, SQLAlchemy, and PostgreSQL that fetches Bitcoin data from Alpha Vantage and performs advanced quantitative analysis.

## Features

- **Real-time Bitcoin Data**: Fetches daily BTC data from Alpha Vantage API
- **Advanced Analytics**: Volume-price correlation analysis with trend detection
- **RESTful API**: Clean, documented endpoints for data access
- **ORM Integration**: SQLAlchemy models with PostgreSQL backend
- **Containerized**: Docker-based deployment for easy scaling
- **Security**: Environment-based configuration for credentials

## Architecture

```
├── api/                 # FastAPI application
│   ├── core/           # Configuration and database setup
│   ├── models/         # SQLAlchemy models and Pydantic schemas
│   ├── routers/        # API endpoints
│   └── services/       # External API integrations
├── calculation/        # Quantitative analysis algorithms
└── db/                # Database migrations and scripts
```

## Quick Start

### 1. Environment Setup

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
```env
# Database Configuration
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_secure_password

# Alpha Vantage API (get from https://www.alphavantage.co/support/#api-key)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key

# Database URL
DATABASE_URL=postgresql://your_user:your_password@postgres:5432/your_db
```

### 2. Run with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 3. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Bitcoin Data
- `GET /btc/data` - Fetch and store latest Bitcoin data
- `GET /btc/history` - Get historical price data
- `GET /btc/analysis` - Get volume-price correlation analysis

### Analysis
- `GET /analysis/volume-price-correlation` - Volume follows price analysis
- `GET /analysis/trends` - Price and volume trend analysis

## Quantitative Analysis

The platform implements sophisticated algorithms to analyze:

1. **Volume-Price Correlation**: Determines if volume changes precede or follow price movements
2. **Trend Analysis**: Identifies bullish/bearish patterns in price and volume
3. **Statistical Significance**: Uses correlation coefficients and statistical tests
4. **Multi-timeframe Analysis**: Analyzes patterns across different time horizons

## Development

### Local Setup (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (ensure PostgreSQL is running)
# Update DATABASE_URL in .env to point to localhost

# Run the application
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Security Notes

- ⚠️ **Never commit `.env` files** - they contain sensitive credentials
- 🔒 **Use strong passwords** for database access
- 🔑 **Rotate API keys** regularly
- 🛡️ **Use HTTPS** in production environments

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `POSTGRES_DB` | Database name | Yes |
| `POSTGRES_USER` | Database username | Yes |
| `POSTGRES_PASSWORD` | Database password | Yes |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API key | Yes |
| `DATABASE_URL` | Full database connection string | Yes |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For issues and questions, please open a GitHub issue with detailed information about the problem.
