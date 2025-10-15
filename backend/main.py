from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta

from database import get_db, engine
from models import Base, Trade, Member, Committee
from schemas import TradeResponse, MemberResponse, CommitteeResponse
from data_collector import collect_congress_data
from routers import trades, members, committees

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Congressional Trading Dashboard API",
    description="API for tracking Congressional and Senate stock trades",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trades.router, prefix="/api/trades", tags=["trades"])
app.include_router(members.router, prefix="/api/members", tags=["members"])
app.include_router(committees.router, prefix="/api/committees", tags=["committees"])

@app.get("/")
async def root():
    return {
        "message": "Congressional Trading Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/collect-data")
async def trigger_data_collection(db: Session = Depends(get_db)):
    """
    Trigger manual data collection from various sources
    """
    try:
        await collect_congress_data(db)
        return {"message": "Data collection completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
