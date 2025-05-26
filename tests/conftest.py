import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set testing environment before importing app
os.environ["TESTING"] = "True"

# Import after setting environment
from api.core.database import Base, get_db  # noqa: E402
from api.main import app  # noqa: E402


class TestConfig:
    """Test configuration and setup utilities"""

    @staticmethod
    def get_test_database_url() -> str:
        return "sqlite:///./test.db"

    @staticmethod
    def get_test_client() -> TestClient:
        """Get FastAPI test client with test database"""
        SQLALCHEMY_DATABASE_URL = TestConfig.get_test_database_url()

        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

        Base.metadata.create_all(bind=engine)

        def override_get_db():
            try:
                db = TestingSessionLocal()
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        return TestClient(app)


@pytest.fixture
def client():
    """Pytest fixture for test client"""
    return TestConfig.get_test_client()


@pytest.fixture
def sample_btc_data():
    """Sample BTC data for testing"""
    return {
        "Meta Data": {
            "1. Information": "Daily Prices and Volumes for Digital Currency",
            "2. Digital Currency Code": "BTC",
            "3. Digital Currency Name": "Bitcoin",
            "4. Market Code": "USD",
            "5. Market Name": "United States Dollar",
            "6. Last Refreshed": "2025-05-26 00:00:00",
            "7. Time Zone": "UTC",
        },
        "Time Series (Digital Currency Daily)": {
            "2025-05-26": {
                "1. open": "109048.41000000",
                "2. high": "109148.11000000",
                "3. low": "108706.04000000",
                "4. close": "108992.36000000",
                "5. volume": "75.94580137",
            },
            "2025-05-25": {
                "1. open": "107794.01000000",
                "2. high": "108200.00000000",
                "3. low": "107500.00000000",
                "4. close": "108000.00000000",
                "5. volume": "82.12345678",
            },
        },
    }


@pytest.fixture
def sample_analysis_data():
    """Sample volume analysis data for testing"""
    return [
        {"date": "2025-05-26", "close_price": 108992.36, "volume": 75.95},
        {"date": "2025-05-25", "close_price": 108000.00, "volume": 82.12},
        {"date": "2025-05-24", "close_price": 107000.00, "volume": 90.50},
    ]
