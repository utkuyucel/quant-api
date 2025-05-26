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

```mermaid
graph TB
    %% External Services
    AV[Alpha Vantage API<br/>Bitcoin Data Provider]
    CLIENT[Client Applications<br/>Web/Mobile/API Consumers]
    
    %% Main Application Layer
    subgraph "FastAPI Application"
        API[FastAPI Router Layer]
        MIDDLEWARE[Middleware & Security]
        
        subgraph "API Endpoints"
            BTC_EP[/btc/* endpoints]
            ANALYSIS_EP[/analysis/* endpoints]
            HEALTH_EP[/health endpoint]
        end
        
        subgraph "Services Layer"
            AV_SERVICE[Alpha Vantage Service<br/>External API Integration]
            BTC_SERVICE[Bitcoin Data Service<br/>Business Logic]
        end
        
        subgraph "Models & Schemas"
            PYDANTIC[Pydantic Schemas<br/>Request/Response Models]
            SQLALCHEMY[SQLAlchemy Models<br/>Database Entities]
        end
        
        subgraph "Core Infrastructure"
            CONFIG[Configuration<br/>Environment Settings]
            DATABASE[Database Connection<br/>SQLAlchemy ORM]
        end
    end
    
    %% Calculation Engine
    subgraph "Quantitative Analysis Engine"
        VOL_ANALYZER[Volume Analyzer<br/>Volume-Price Correlation]
        TREND_ANALYZER[Trend Analyzer<br/>Pattern Detection]
        STAT_ENGINE[Statistical Engine<br/>Correlation & Significance Tests]
    end
    
    %% Data Persistence
    subgraph "PostgreSQL Database"
        BTC_TABLE[Bitcoin Data Table<br/>Daily OHLCV Data]
        ANALYSIS_TABLE[Analysis Results Table<br/>Computed Metrics]
        METADATA_TABLE[Metadata Tables<br/>System State]
    end
    
    %% Data Flow
    CLIENT --> API
    API --> MIDDLEWARE
    MIDDLEWARE --> BTC_EP
    MIDDLEWARE --> ANALYSIS_EP
    MIDDLEWARE --> HEALTH_EP
    
    BTC_EP --> BTC_SERVICE
    ANALYSIS_EP --> BTC_SERVICE
    
    BTC_SERVICE --> AV_SERVICE
    BTC_SERVICE --> VOL_ANALYZER
    BTC_SERVICE --> TREND_ANALYZER
    
    AV_SERVICE --> AV
    
    VOL_ANALYZER --> STAT_ENGINE
    TREND_ANALYZER --> STAT_ENGINE
    
    BTC_SERVICE --> DATABASE
    DATABASE --> BTC_TABLE
    DATABASE --> ANALYSIS_TABLE
    DATABASE --> METADATA_TABLE
    
    %% Configuration Flow
    CONFIG -.-> DATABASE
    CONFIG -.-> AV_SERVICE
    
    %% Schema Validation
    PYDANTIC -.-> API
    SQLALCHEMY -.-> DATABASE
    
    %% External Dependencies
    AV -.->|Bitcoin OHLCV Data| AV_SERVICE
    
    %% Docker Infrastructure
    subgraph "Docker Environment"
        DOCKER_API[quant-api Container<br/>FastAPI + Python]
        DOCKER_DB[postgres Container<br/>PostgreSQL Database]
        DOCKER_NET[Docker Network<br/>Internal Communication]
    end
    
    DATABASE -.-> DOCKER_DB
    API -.-> DOCKER_API
    DOCKER_API -.-> DOCKER_NET
    DOCKER_DB -.-> DOCKER_NET
    
    %% Styling
    classDef external fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef api fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef analysis fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef database fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef docker fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    
    class AV,CLIENT external
    class API,MIDDLEWARE,BTC_EP,ANALYSIS_EP,HEALTH_EP,AV_SERVICE,BTC_SERVICE,PYDANTIC,SQLALCHEMY,CONFIG,DATABASE api
    class VOL_ANALYZER,TREND_ANALYZER,STAT_ENGINE analysis
    class BTC_TABLE,ANALYSIS_TABLE,METADATA_TABLE database
    class DOCKER_API,DOCKER_DB,DOCKER_NET docker
```

### Directory Structure
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
