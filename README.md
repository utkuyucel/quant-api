# Quant API - Bitcoin Analysis Platform

FastAPI-based Bitcoin quantitative analysis platform that fetches real-time data and performs advanced statistical analysis.

## What It Does

- 📈 **Fetches Bitcoin Data**: Real-time OHLCV data from Alpha Vantage API
- 📊 **Quantitative Analysis**: Volume-price correlation and trend detection
- 🔌 **REST API**: Clean endpoints for data access and analysis results
- 🐳 **Ready to Deploy**: Docker containerization with PostgreSQL

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WebApp[Web Application]
        Mobile[Mobile App]
        API_Client[API Client]
    end
    
    subgraph "API Gateway"
        FastAPI[FastAPI Server]
        Auth[Authentication]
        Rate[Rate Limiting]
    end
    
    subgraph "Business Logic"
        BTC_Service[Bitcoin Data Service]
        Analysis_Service[Analysis Engine]
        Cache[Redis Cache]
    end
    
    subgraph "Data Processing"
        Fetcher[Data Fetcher]
        Validator[Data Validator]
        Analyzer[Volume-Price Analyzer]
        Stats[Statistical Calculator]
    end
    
    subgraph "Data Storage"
        PostgreSQL[(PostgreSQL)]
        TimeSeries[(Time Series Data)]
        Results[(Analysis Results)]
    end
    
    subgraph "External APIs"
        AlphaVantage[Alpha Vantage API]
        Backup[Backup Data Source]
    end
    
    WebApp --> FastAPI
    Mobile --> FastAPI
    API_Client --> FastAPI
    
    FastAPI --> Auth
    Auth --> Rate
    Rate --> BTC_Service
    Rate --> Analysis_Service
    
    BTC_Service --> Cache
    BTC_Service --> Fetcher
    Analysis_Service --> Analyzer
    
    Fetcher --> Validator
    Validator --> PostgreSQL
    Analyzer --> Stats
    Stats --> Results
    
    Fetcher --> AlphaVantage
    Fetcher --> Backup
    
    PostgreSQL --> TimeSeries
    Analysis_Service --> PostgreSQL
```

## Data Flow & Analysis Pipeline

```mermaid
sequenceDiagram
    participant C as Client
    participant API as FastAPI
    participant BTC as Bitcoin Service
    participant AV as Alpha Vantage
    participant DB as PostgreSQL
    participant AN as Analysis Engine
    participant VA as Volume Analyzer
    
    Note over C,VA: Bitcoin Data Fetching Flow
    C->>API: GET /btc/data
    API->>BTC: fetch_latest_data()
    BTC->>AV: request OHLCV data
    AV-->>BTC: Bitcoin price/volume data
    BTC->>DB: store raw data
    DB-->>BTC: confirmation
    BTC-->>API: success response
    API-->>C: JSON data
    
    Note over C,VA: Analysis Flow
    C->>API: GET /analysis/correlation
    API->>AN: analyze_volume_price()
    AN->>DB: query historical data
    DB-->>AN: OHLCV dataset
    AN->>VA: calculate correlation
    VA->>VA: statistical analysis
    VA-->>AN: correlation results
    AN->>DB: save analysis results
    AN-->>API: analysis report
    API-->>C: correlation insights
```

## Quantitative Analysis Components

```mermaid
graph LR
    subgraph "Data Input"
        OHLC[OHLC Prices]
        Volume[Trading Volume]
        Time[Timestamps]
    end
    
    subgraph "Analysis Algorithms"
        Correlation[Volume-Price Correlation]
        Trend[Trend Detection]
        Stats[Statistical Tests]
        Signals[Trading Signals]
    end
    
    subgraph "Output Metrics"
        Coeff[Correlation Coefficient]
        PValue[P-Value]
        Trend_Dir[Trend Direction]
        Confidence[Confidence Level]
    end
    
    OHLC --> Correlation
    Volume --> Correlation
    Time --> Trend
    
    Correlation --> Stats
    Trend --> Stats
    
    Stats --> Coeff
    Stats --> PValue
    Stats --> Trend_Dir
    Stats --> Confidence
    
    Correlation --> Signals
    Trend --> Signals
```

## Docker Deployment Architecture

```mermaid
graph TB
    subgraph "Docker Network"
        subgraph "Application Container"
            FastAPI[FastAPI App:8000]
            Workers[Uvicorn Workers]
            Config[Environment Config]
        end
        
        subgraph "Database Container"
            PostgreSQL[PostgreSQL:5432]
            DataVolume[Persistent Volume]
        end
        
        subgraph "Cache Layer (Optional)"
            Redis[Redis:6379]
            CacheVolume[Cache Storage]
        end
    end
    
    subgraph "External Services"
        AlphaVantage[Alpha Vantage API]
        Monitoring[Health Monitoring]
    end
    
    FastAPI --> PostgreSQL
    FastAPI --> Redis
    FastAPI --> AlphaVantage
    PostgreSQL --> DataVolume
    Redis --> CacheVolume
    Monitoring --> FastAPI
    
    Config -.-> FastAPI
    Workers -.-> FastAPI
```

## Quick Start

1. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Alpha Vantage API key and database credentials
   ```

2. **Run with Docker**
   ```bash
   docker-compose up --build
   ```

3. **Access API**
   - 📖 Documentation: http://localhost:8000/docs
   - ❤️ Health Check: http://localhost:8000/health

## API Endpoints & Features

```mermaid
graph LR
    subgraph "Bitcoin Data Endpoints"
        A[GET /btc/data] --> A1[Fetch Latest Data]
        B[GET /btc/history] --> B1[Historical Prices]
    end
    
    subgraph "Analysis Endpoints"
        C[GET /analysis/volume-price-correlation] --> C1[Volume Analysis]
        D[GET /analysis/trends] --> D1[Trend Detection]
    end
    
    subgraph "System Endpoints"
        E[GET /health] --> E1[Health Check]
        F[GET /docs] --> F1[API Documentation]
    end
    
    A1 --> DataStorage[(Database)]
    B1 --> DataStorage
    C1 --> AnalysisResults[(Analysis Results)]
    D1 --> AnalysisResults
```

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/btc/data` | GET | Fetch latest Bitcoin data | OHLCV JSON data |
| `/btc/history` | GET | Get historical price data | Time series data |
| `/analysis/volume-price-correlation` | GET | Volume-price analysis | Correlation metrics |
| `/analysis/trends` | GET | Price and volume trends | Trend analysis |
| `/health` | GET | Health check | System status |
| `/docs` | GET | API documentation | Interactive docs |

## Analysis Features

- **Volume-Price Correlation**: Does volume lead or follow price?
- **Trend Detection**: Identify bullish/bearish patterns
- **Statistical Significance**: Correlation coefficients and tests

## Development

**Local Setup**
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

**Database Migrations**
```bash
alembic upgrade head  # Apply migrations
```

## Required Environment Variables

| Variable | Get From |
|----------|----------|
| `ALPHA_VANTAGE_API_KEY` | [alphavantage.co](https://www.alphavantage.co/support/#api-key) |
| `DATABASE_URL` | Your PostgreSQL connection string |

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Database
- **Docker** - Containerization
- **NumPy** - Numerical computing for analysis

---

**License**: MIT | **Issues**: [GitHub Issues](../../issues)
