from datetime import datetime
from functools import lru_cache
from typing import Any

import httpx

from api.core.config import get_settings


class AlphaVantageService:
    """Service to fetch data from Alpha Vantage API"""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://www.alphavantage.co/query"

    async def fetch_btc_daily_data(self) -> dict[str, Any]:
        """Fetch daily BTC data from Alpha Vantage"""
        params = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": "BTC",
            "market": "USD",
            "apikey": self.settings.alpha_vantage_api_key
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]

    def parse_btc_data(self, raw_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse raw Alpha Vantage response into structured data"""
        if "Time Series (Digital Currency Daily)" not in raw_data:
            raise ValueError("Invalid API response format")

        time_series = raw_data["Time Series (Digital Currency Daily)"]
        parsed_data = []

        for date_str, data in time_series.items():
            parsed_data.append({
                "date": datetime.strptime(date_str, "%Y-%m-%d"),
                "close_price": float(data["4. close"]),
                "volume": float(data["5. volume"])
            })

        # Sort by date ascending for calculations
        return sorted(parsed_data, key=lambda x: x["date"])


@lru_cache
def get_alpha_vantage_service() -> AlphaVantageService:
    return AlphaVantageService()
