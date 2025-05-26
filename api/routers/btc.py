from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.models.btc_models import BTCData
from api.models.schemas import BTCDataResponse
from api.services.alpha_vantage import get_alpha_vantage_service

router = APIRouter()


@router.post("/fetch-data", response_model=dict, summary="Fetch latest BTC data")
async def fetch_btc_data(db: Session = Depends(get_db)) -> dict[str, str | int]:
    """Fetch latest Bitcoin data from Alpha Vantage and store in database"""
    try:
        service = get_alpha_vantage_service()
        raw_data = await service.fetch_btc_daily_data()
        parsed_data = service.parse_btc_data(raw_data)

        records_added = 0
        for data_point in parsed_data:
            # Check if record already exists
            existing = db.query(BTCData).filter(BTCData.date == data_point["date"]).first()
            if not existing:
                btc_record = BTCData(**data_point)
                db.add(btc_record)
                records_added += 1

        db.commit()
        return {
            "message": "Data fetched successfully",
            "records_added": records_added,
            "total_records": len(parsed_data)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}") from e


@router.get("/history", response_model=list[BTCDataResponse], summary="Get historical BTC data")
def get_btc_history(
    limit: int = 30,
    days_back: int = 30,
    db: Session = Depends(get_db)
) -> list[BTCData]:
    """Get historical Bitcoin data from the database"""
    cutoff_date = datetime.now() - timedelta(days=days_back)

    data = db.query(BTCData).filter(
        BTCData.date >= cutoff_date
    ).order_by(BTCData.date.desc()).limit(limit).all()

    if not data:
        raise HTTPException(status_code=404, detail="No data found")

    return data


@router.get("/latest", response_model=BTCDataResponse, summary="Get latest BTC data")
def get_latest_btc_data(db: Session = Depends(get_db)) -> BTCData:
    """Get the most recent Bitcoin data point"""
    latest = db.query(BTCData).order_by(BTCData.date.desc()).first()

    if not latest:
        raise HTTPException(status_code=404, detail="No data found")

    return latest


@router.get("/stats", summary="Get BTC data statistics")
def get_btc_stats(db: Session = Depends(get_db)) -> dict[str, str | int | float | None]:
    """Get basic statistics about stored Bitcoin data"""
    total_records = db.query(BTCData).count()

    if total_records == 0:
        return {"message": "No data available", "total_records": 0}

    latest = db.query(BTCData).order_by(BTCData.date.desc()).first()
    oldest = db.query(BTCData).order_by(BTCData.date.asc()).first()

    return {
        "total_records": total_records,
        "latest_date": latest.date.isoformat() if latest else None,
        "oldest_date": oldest.date.isoformat() if oldest else None,
        "latest_price": float(latest.close_price) if latest else None,
        "date_range_days": (latest.date - oldest.date).days if latest and oldest else 0
    }
