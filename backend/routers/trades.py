from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models import Trade, Member
from schemas import TradeResponse, TradeWithMember, TradeFilter, DashboardStats
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[TradeWithMember])
async def get_trades(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    member_id: Optional[int] = None,
    chamber: Optional[str] = None,
    party: Optional[str] = None,
    ticker: Optional[str] = None,
    transaction_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Get trades with optional filtering
    """
    query = db.query(Trade).join(Member)
    
    # Apply filters
    if member_id:
        query = query.filter(Trade.member_id == member_id)
    if chamber:
        query = query.filter(Member.chamber == chamber)
    if party:
        query = query.filter(Member.party == party)
    if ticker:
        query = query.filter(Trade.ticker.ilike(f"%{ticker}%"))
    if transaction_type:
        query = query.filter(Trade.transaction_type == transaction_type)
    if start_date:
        query = query.filter(Trade.transaction_date >= start_date)
    if end_date:
        query = query.filter(Trade.transaction_date <= end_date)
    if min_amount:
        query = query.filter(
            or_(
                Trade.amount_exact >= min_amount,
                Trade.amount_min >= min_amount
            )
        )
    if max_amount:
        query = query.filter(
            or_(
                Trade.amount_exact <= max_amount,
                Trade.amount_max <= max_amount
            )
        )
    
    # Order by transaction date (most recent first)
    trades = query.order_by(Trade.transaction_date.desc()).offset(skip).limit(limit).all()
    
    return trades

@router.get("/recent", response_model=List[TradeWithMember])
async def get_recent_trades(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get recent trades within specified days
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    trades = db.query(Trade).join(Member).filter(
        Trade.transaction_date >= start_date
    ).order_by(Trade.transaction_date.desc()).limit(limit).all()
    
    return trades

@router.get("/by-member/{member_id}", response_model=List[TradeResponse])
async def get_trades_by_member(
    member_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all trades for a specific member
    """
    trades = db.query(Trade).filter(
        Trade.member_id == member_id
    ).order_by(Trade.transaction_date.desc()).offset(skip).limit(limit).all()
    
    return trades

@router.get("/by-ticker/{ticker}", response_model=List[TradeWithMember])
async def get_trades_by_ticker(
    ticker: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all trades for a specific stock ticker
    """
    trades = db.query(Trade).join(Member).filter(
        Trade.ticker.ilike(f"%{ticker.upper()}%")
    ).order_by(Trade.transaction_date.desc()).offset(skip).limit(limit).all()
    
    return trades

@router.get("/stats", response_model=DashboardStats)
async def get_trading_stats(db: Session = Depends(get_db)):
    """
    Get dashboard statistics
    """
    # Total trades
    total_trades = db.query(Trade).count()
    
    # Total members
    total_members = db.query(Member).count()
    
    # Total committees (placeholder - will be implemented when committee data is added)
    total_committees = 0
    
    # Recent trades (last 30 days)
    recent_date = datetime.utcnow() - timedelta(days=30)
    recent_trades_count = db.query(Trade).filter(
        Trade.transaction_date >= recent_date
    ).count()
    
    # Top traded stocks
    top_stocks = db.query(
        Trade.ticker,
        func.count(Trade.id).label('trade_count')
    ).group_by(Trade.ticker).order_by(
        func.count(Trade.id).desc()
    ).limit(10).all()
    
    top_traded_stocks = [
        {"ticker": stock.ticker, "trade_count": stock.trade_count}
        for stock in top_stocks
    ]
    
    # Trades by chamber
    trades_by_chamber = db.query(
        Member.chamber,
        func.count(Trade.id).label('trade_count')
    ).join(Trade).group_by(Member.chamber).all()
    
    trades_by_chamber_dict = {
        chamber.chamber: chamber.trade_count
        for chamber in trades_by_chamber
    }
    
    # Trades by party
    trades_by_party = db.query(
        Member.party,
        func.count(Trade.id).label('trade_count')
    ).join(Trade).group_by(Member.party).all()
    
    trades_by_party_dict = {
        party.party: party.trade_count
        for party in trades_by_party
    }
    
    return DashboardStats(
        total_trades=total_trades,
        total_members=total_members,
        total_committees=total_committees,
        recent_trades_count=recent_trades_count,
        top_traded_stocks=top_traded_stocks,
        trades_by_chamber=trades_by_chamber_dict,
        trades_by_party=trades_by_party_dict
    )

@router.get("/{trade_id}", response_model=TradeWithMember)
async def get_trade(trade_id: int, db: Session = Depends(get_db)):
    """
    Get a specific trade by ID
    """
    trade = db.query(Trade).join(Member).filter(Trade.id == trade_id).first()
    
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    return trade
