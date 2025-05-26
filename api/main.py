from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.database import Base, engine
from api.routers import analysis, btc

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quant API - Bitcoin Analysis Platform",
    description="A comprehensive API for Bitcoin data analysis with advanced quantitative algorithms",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(btc.router, prefix="/btc", tags=["Bitcoin Data"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])


@app.get("/", summary="Root endpoint")
async def root() -> dict[str, str]:
    """Root endpoint providing API information"""
    return {
        "message": "Quant API - Bitcoin Analysis Platform",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", summary="Health check")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy", "service": "quant-api"}
