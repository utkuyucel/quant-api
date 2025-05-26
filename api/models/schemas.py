from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class BTCDataBase(BaseModel):
    date: datetime
    close_price: float
    volume: float


class BTCDataCreate(BTCDataBase):
    pass


class BTCDataResponse(BTCDataBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class VolumeAnalysisBase(BaseModel):
    date: datetime
    price_change_pct: float
    volume_change_pct: float
    volume_follows_price: str
    strength_score: float
    trend_direction: str


class VolumeAnalysisCreate(VolumeAnalysisBase):
    pass


class VolumeAnalysisResponse(VolumeAnalysisBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class AnalysisResult(BaseModel):
    """Comprehensive analysis result"""
    total_records: int
    latest_analysis: VolumeAnalysisResponse | None
    summary: dict[str, Any]
    recommendations: list[str]
