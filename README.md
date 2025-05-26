# Quant API - Bitcoin Analysis Platform

FastAPI-based Bitcoin quantitative analysis platform that fetches real-time data and performs advanced statistical analysis.

## What It Does

- 📈 **Fetches Bitcoin Data**: Real-time OHLCV data from Alpha Vantage API
- 📊 **Quantitative Analysis**: Volume-price correlation and trend detection
- 🔌 **REST API**: Clean endpoints for data access and analysis results
- 🐳 **Ready to Deploy**: Docker containerization with PostgreSQL

## Architecture & Workflow

```mermaid
graph TD
    A[Client Apps] --> B[FastAPI Router]
    B --> C[Bitcoin Service]
    B --> D[Analysis Service]
    C --> E[Alpha Vantage API]
    C --> F[PostgreSQL Database]
    D --> F
    D --> G[Volume Analyzer]
    G --> H[Statistical Engine]
    H --> D
    D --> B
    B --> A
    
    subgraph Docker [Docker Container]
        B
        C
        D
        G
        H
        F
    end
```

### Workflow Steps
1. **Client Request** → FastAPI receives API call
2. **Route to Service** → Request routed to Bitcoin or Analysis service
3. **Fetch Data** → Bitcoin service gets data from Alpha Vantage API
4. **Store Data** → Raw Bitcoin data saved to PostgreSQL
5. **Read Data** → Analysis service reads stored data
6. **Process Analysis** → Volume analyzer processes the data
7. **Calculate Stats** → Statistical engine computes correlations
8. **Save Results** → Analysis results stored in database
9. **Return Response** → JSON data sent back to client

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

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /btc/data` | Fetch latest Bitcoin data |
| `GET /btc/history` | Get historical price data |
| `GET /analysis/volume-price-correlation` | Volume-price analysis |
| `GET /analysis/trends` | Price and volume trends |

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
