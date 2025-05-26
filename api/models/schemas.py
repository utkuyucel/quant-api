from datetime import datetime

from pydantic import BaseModel


class BTCDataBase(BaseModel):
    date: datetime
    close_price: float
    volume: float


class BTCDataCreate(BTCDataBase):
    pass


class BTCDataResponse(BTCDataBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisResult(BaseModel):
    """Comprehensive analysis result"""
    total_records: int
    latest_analysis: VolumeAnalysisResponse | None
    summary: dict
    recommendations: list[str]
