from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.models.btc_models import BTCData, VolumeAnalysis
from api.models.schemas import AnalysisResult, VolumeAnalysisResponse
from calculation.volume_analyzer import get_volume_analyzer

router = APIRouter()


@router.post("/run-volume-analysis", summary="Run volume-price correlation analysis")
async def run_volume_analysis(
    lookback_period: int = Query(14, ge=7, le=50, description="Analysis lookback period"),
    min_periods: int = Query(7, ge=3, le=20, description="Minimum periods for analysis"),
    db: Session = Depends(get_db)
) -> dict[str, str | int]:
    """Run comprehensive volume-price correlation analysis and store results"""

    # Fetch historical data
    btc_data = db.query(BTCData).order_by(BTCData.date.asc()).all()

    if len(btc_data) < min_periods:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient data. Need at least {min_periods} records"
        )

    # Convert to analysis format
    data_for_analysis = [
        {
            "date": record.date,
            "close_price": record.close_price,
            "volume": record.volume
        }
        for record in btc_data
    ]

    # Run analysis
    analyzer = get_volume_analyzer(lookback_period, min_periods)
    analysis_results = analyzer.analyze_volume_price_correlation(data_for_analysis)

    if not analysis_results:
        raise HTTPException(status_code=400, detail="No analysis results generated")

    # Store results in database
    records_added = 0
    for i, result in enumerate(analysis_results):
        # Get corresponding date from original data
        data_index = min_periods + i
        if data_index < len(btc_data):
            analysis_date = btc_data[data_index].date

            # Check if analysis already exists for this date
            existing = db.query(VolumeAnalysis).filter(
                VolumeAnalysis.date == analysis_date
            ).first()

            if not existing:
                volume_analysis = VolumeAnalysis(
                    date=analysis_date,
                    price_change_pct=result.price_change_pct,
                    volume_change_pct=result.volume_change_pct,
                    volume_follows_price=result.volume_follows_price,
                    strength_score=result.strength_score,
                    trend_direction=result.trend_direction
                )
                db.add(volume_analysis)
                records_added += 1

    try:
        db.commit()
        return {
            "message": "Volume analysis completed successfully",
            "records_analyzed": len(analysis_results),
            "records_added": records_added
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to store analysis: {str(e)}") from e


@router.get("/volume-price-correlation", response_model=list[VolumeAnalysisResponse])
def get_volume_analysis(
    limit: int = Query(30, ge=1, le=100, description="Number of records to return"),
    days_back: int = Query(30, ge=1, le=365, description="Days to look back"),
    db: Session = Depends(get_db)
) -> list[VolumeAnalysis]:
    """Get volume-price correlation analysis results"""
    cutoff_date = datetime.now() - timedelta(days=days_back)

    analyses = db.query(VolumeAnalysis).filter(
        VolumeAnalysis.date >= cutoff_date
    ).order_by(VolumeAnalysis.date.desc()).limit(limit).all()

    if not analyses:
        raise HTTPException(status_code=404, detail="No analysis data found")

    return analyses


@router.get("/summary", response_model=AnalysisResult)
def get_analysis_summary(
    days_back: int = Query(30, ge=1, le=365, description="Days to look back"),
    db: Session = Depends(get_db)
) -> AnalysisResult:
    """Get comprehensive analysis summary with insights and recommendations"""
    cutoff_date = datetime.now() - timedelta(days=days_back)

    analyses = db.query(VolumeAnalysis).filter(
        VolumeAnalysis.date >= cutoff_date
    ).order_by(VolumeAnalysis.date.desc()).all()

    if not analyses:
        raise HTTPException(status_code=404, detail="No analysis data found")

    # Calculate summary statistics
    total_records = len(analyses)
    latest_analysis = analyses[0] if analyses else None

    # Generate insights
    positive_correlations = len([a for a in analyses if a.volume_follows_price == "positive"])
    negative_correlations = len([a for a in analyses if a.volume_follows_price == "negative"])
    divergent_cases = len([a for a in analyses if a.volume_follows_price == "divergent"])

    avg_strength = sum(a.strength_score for a in analyses) / total_records

    up_trends = len([a for a in analyses if a.trend_direction == "up"])
    down_trends = len([a for a in analyses if a.trend_direction == "down"])
    sideways_trends = len([a for a in analyses if a.trend_direction == "sideways"])

    summary = {
        "total_records": total_records,
        "positive_correlations_pct": round((positive_correlations / total_records) * 100, 2),
        "negative_correlations_pct": round((negative_correlations / total_records) * 100, 2),
        "divergent_cases_pct": round((divergent_cases / total_records) * 100, 2),
        "average_strength_score": round(avg_strength, 3),
        "trend_distribution": {
            "up_pct": round((up_trends / total_records) * 100, 2),
            "down_pct": round((down_trends / total_records) * 100, 2),
            "sideways_pct": round((sideways_trends / total_records) * 100, 2)
        }
    }

    # Generate recommendations
    recommendations = _generate_recommendations(
        positive_correlations, negative_correlations, divergent_cases,
        total_records, float(avg_strength), latest_analysis
    )

    return AnalysisResult(
        total_records=total_records,
        latest_analysis=latest_analysis,
        summary=summary,
        recommendations=recommendations
    )


def _generate_recommendations(
    positive: int, _negative: int, divergent: int,
    total: int, avg_strength: float, latest: VolumeAnalysis | None
) -> list[str]:
    """Generate trading recommendations based on analysis"""
    recommendations = []

    positive_pct = (positive / total) * 100
    divergent_pct = (divergent / total) * 100

    # Market sentiment recommendations
    if positive_pct > 60:
        recommendations.append("Strong volume-price correlation detected. Market shows healthy price discovery.")
    elif divergent_pct > 50:
        recommendations.append("High divergence between volume and price. Market may be in transition.")

    # Strength-based recommendations
    if avg_strength > 0.7:
        recommendations.append("High confidence in volume patterns. Technical indicators likely reliable.")
    elif avg_strength < 0.3:
        recommendations.append("Low confidence in volume patterns. Use additional confirmation signals.")

    # Current trend recommendations
    if latest:
        if latest.trend_direction == "up" and latest.volume_follows_price == "positive":
            recommendations.append("Bullish trend with volume confirmation. Consider long positions.")
        elif latest.trend_direction == "down" and latest.volume_follows_price == "positive":
            recommendations.append("Bearish trend with volume confirmation. Exercise caution on long positions.")
        elif latest.volume_follows_price == "divergent":
            recommendations.append("Volume divergence detected. Monitor for potential trend reversal.")

    if not recommendations:
        recommendations.append("Mixed signals detected. Maintain balanced risk management approach.")

    return recommendations


@router.get("/trends", summary="Get trend analysis")
def get_trend_analysis(
    days_back: int = Query(30, ge=1, le=365, description="Days to look back"),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    """Get detailed trend analysis with volume patterns"""
    cutoff_date = datetime.now() - timedelta(days=days_back)

    analyses = db.query(VolumeAnalysis).filter(
        VolumeAnalysis.date >= cutoff_date
    ).order_by(VolumeAnalysis.date.asc()).all()

    if not analyses:
        raise HTTPException(status_code=404, detail="No analysis data found")

    # Calculate trend statistics
    trend_changes = []
    for i in range(1, len(analyses)):
        prev_trend = analyses[i-1].trend_direction
        curr_trend = analyses[i].trend_direction
        if prev_trend != curr_trend:
            trend_changes.append({
                "date": analyses[i].date.isoformat(),
                "from": prev_trend,
                "to": curr_trend,
                "volume_relationship": analyses[i].volume_follows_price,
                "strength": analyses[i].strength_score
            })

    return {
        "period_days": days_back,
        "total_trend_changes": len(trend_changes),
        "trend_changes": trend_changes[-10:],  # Last 10 changes
        "current_trend": analyses[-1].trend_direction if analyses else "unknown",
        "current_volume_relationship": analyses[-1].volume_follows_price if analyses else "unknown"
    }
