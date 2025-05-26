from sqlalchemy import Column, DateTime, Float, Index, Integer, String
from sqlalchemy.sql import func

from api.core.database import Base


class BTCData(Base):
    __tablename__ = "btc_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, index=True, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_btc_date_desc', 'date', postgresql_using='btree'),
    )


class VolumeAnalysis(Base):
    __tablename__ = "volume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    price_change_pct = Column(Float, nullable=False)
    volume_change_pct = Column(Float, nullable=False)
    volume_follows_price = Column(String, nullable=False)  # "positive", "negative", "divergent"
    strength_score = Column(Float, nullable=False)  # 0-1 score
    trend_direction = Column(String, nullable=False)  # "up", "down", "sideways"
    created_at = Column(DateTime, default=func.now())

    __table_args__ = (
        Index('idx_analysis_date_desc', 'date', postgresql_using='btree'),
    )
