from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from database import get_db
from models import Member, Trade
from schemas import MemberResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[MemberResponse])
async def get_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    chamber: Optional[str] = None,
    party: Optional[str] = None,
    state: Optional[str] = None,
    has_trades: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get members with optional filtering
    """
    query = db.query(Member)
    
    # Apply filters
    if chamber:
        query = query.filter(Member.chamber == chamber)
    if party:
        query = query.filter(Member.party == party)
    if state:
        query = query.filter(Member.state == state)
    if has_trades is not None:
        if has_trades:
            query = query.filter(Member.trades.any())
        else:
            query = query.filter(~Member.trades.any())
    
    # Order by name
    members = query.order_by(Member.name).offset(skip).limit(limit).all()
    
    return members

@router.get("/by-chamber/{chamber}", response_model=List[MemberResponse])
async def get_members_by_chamber(
    chamber: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get members by chamber (House or Senate)
    """
    if chamber.lower() not in ['house', 'senate']:
        raise HTTPException(status_code=400, detail="Chamber must be 'House' or 'Senate'")
    
    members = db.query(Member).filter(
        Member.chamber == chamber.title()
    ).order_by(Member.name).offset(skip).limit(limit).all()
    
    return members

@router.get("/by-state/{state}", response_model=List[MemberResponse])
async def get_members_by_state(
    state: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get members by state
    """
    members = db.query(Member).filter(
        Member.state == state.upper()
    ).order_by(Member.name).offset(skip).limit(limit).all()
    
    return members

@router.get("/by-party/{party}", response_model=List[MemberResponse])
async def get_members_by_party(
    party: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get members by political party
    """
    members = db.query(Member).filter(
        Member.party == party
    ).order_by(Member.name).offset(skip).limit(limit).all()
    
    return members

@router.get("/most-active", response_model=List[MemberResponse])
async def get_most_active_traders(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get members with the most trades
    """
    # Get members ordered by number of trades
    members = db.query(Member).join(Trade).group_by(Member.id).order_by(
        func.count(Trade.id).desc()
    ).limit(limit).all()
    
    return members

@router.get("/{member_id}", response_model=MemberResponse)
async def get_member(member_id: int, db: Session = Depends(get_db)):
    """
    Get a specific member by ID
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return member

@router.get("/search/{name}", response_model=List[MemberResponse])
async def search_members(
    name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search members by name
    """
    members = db.query(Member).filter(
        Member.name.ilike(f"%{name}%")
    ).order_by(Member.name).offset(skip).limit(limit).all()
    
    return members
