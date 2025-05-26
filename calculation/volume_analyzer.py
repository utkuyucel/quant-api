from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray


@dataclass(frozen=True)
class VolumeAnalysisResult:
    """Immutable result object for volume analysis"""
    correlation: float
    volume_follows_price: str
    strength_score: float
    trend_direction: str
    price_change_pct: float
    volume_change_pct: float
    confidence_level: float


class VolumeAnalyzer:
    """Advanced quantitative analyzer for volume-price relationships"""

    def __init__(self, lookback_period: int = 14, min_periods: int = 7):
        self.lookback_period = lookback_period
        self.min_periods = min_periods

    def analyze_volume_price_correlation(self, data: list[dict[str, Any]]) -> list[VolumeAnalysisResult]:
        """
        Analyze volume-price correlation using rolling windows and statistical measures.
        Returns analysis for each data point where sufficient history exists.
        """
        if len(data) < self.min_periods:
            return []

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        # Calculate percentage changes
        df['price_change_pct'] = df['close_price'].pct_change()
        df['volume_change_pct'] = df['volume'].pct_change()

        results = []

        for i in range(self.min_periods, len(df)):
            # Get rolling window data
            window_data = df.iloc[max(0, i - self.lookback_period + 1):i + 1]

            if len(window_data) < self.min_periods:
                continue

            result = self._calculate_single_analysis(window_data, i)
            if result:
                results.append(result)

        return results

    def _calculate_single_analysis(self, window_data: pd.DataFrame, _current_idx: int) -> VolumeAnalysisResult | None:
        """Calculate analysis for a single time point"""
        # Remove NaN values for correlation calculation
        clean_data = window_data.dropna(subset=['price_change_pct', 'volume_change_pct'])

        if len(clean_data) < self.min_periods:
            return None

        price_changes = clean_data['price_change_pct'].values
        volume_changes = clean_data['volume_change_pct'].values

        # Calculate correlation
        correlation = float(np.corrcoef(price_changes, volume_changes)[0, 1])
        if np.isnan(correlation):
            correlation = 0.0

        # Current period changes
        current_price_change = window_data.iloc[-1]['price_change_pct']
        current_volume_change = window_data.iloc[-1]['volume_change_pct']

        # Determine volume-price relationship
        volume_follows_price = self._determine_volume_relationship(
            correlation, current_price_change, current_volume_change
        )

        # Calculate strength score (0-1)
        strength_score = self._calculate_strength_score(
            correlation, price_changes, volume_changes
        )

        # Determine trend direction
        trend_direction = self._determine_trend_direction(window_data)

        # Calculate confidence level
        confidence_level = self._calculate_confidence_level(clean_data, correlation)

        return VolumeAnalysisResult(
            correlation=correlation,
            volume_follows_price=volume_follows_price,
            strength_score=strength_score,
            trend_direction=trend_direction,
            price_change_pct=current_price_change,
            volume_change_pct=current_volume_change,
            confidence_level=confidence_level
        )

    def _determine_volume_relationship(
        self, correlation: float, price_change: float, volume_change: float
    ) -> str:
        """Determine if volume follows price direction"""
        if abs(correlation) < 0.1:
            return "divergent"

        # Check if volume and price move in same direction
        same_direction = (price_change > 0 and volume_change > 0) or \
                        (price_change < 0 and volume_change < 0)

        if correlation > 0.3 and same_direction:
            return "positive"
        elif correlation < -0.3 and not same_direction:
            return "negative"
        else:
            return "divergent"

    def _calculate_strength_score(
        self, correlation: float, price_changes: NDArray[np.floating[Any]], volume_changes: NDArray[np.floating[Any]]
    ) -> float:
        """Calculate strength score based on correlation and volatility"""
        # Base score from correlation strength
        base_score = float(min(abs(correlation), 1.0))

        # Adjust for consistency (lower volatility = higher score)
        price_volatility = np.std(price_changes) if len(price_changes) > 1 else 1.0
        volume_volatility = np.std(volume_changes) if len(volume_changes) > 1 else 1.0

        # Normalize volatility adjustment (0.5 to 1.0 range)
        volatility_adjustment = 1.0 / (1.0 + (price_volatility + volume_volatility) / 2)
        volatility_adjustment = 0.5 + 0.5 * volatility_adjustment

        return float(base_score * volatility_adjustment)

    def _determine_trend_direction(self, window_data: pd.DataFrame) -> str:
        """Determine overall trend direction using simple moving average"""
        prices = window_data['close_price'].values

        if len(prices) < 3:
            return "sideways"

        # Compare recent prices with earlier prices
        recent_avg = np.mean(prices[-3:])
        earlier_avg = np.mean(prices[:3])

        change_pct = (recent_avg - earlier_avg) / earlier_avg

        if change_pct > 0.02:  # 2% threshold
            return "up"
        elif change_pct < -0.02:
            return "down"
        else:
            return "sideways"

    def _calculate_confidence_level(self, data: pd.DataFrame, correlation: float) -> float:
        """Calculate confidence level based on data quality and sample size"""
        sample_size = len(data)

        # Base confidence from sample size (more data = higher confidence)
        size_confidence = min(sample_size / (self.lookback_period * 2), 1.0)

        # Adjust for correlation strength
        correlation_confidence = abs(correlation)

        # Combine factors
        return (size_confidence + correlation_confidence) / 2


@lru_cache(maxsize=128)
def get_volume_analyzer(lookback_period: int = 14, min_periods: int = 7) -> VolumeAnalyzer:
    """Get cached volume analyzer instance"""
    return VolumeAnalyzer(lookback_period, min_periods)
