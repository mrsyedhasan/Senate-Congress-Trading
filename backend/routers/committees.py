from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Committee, CommitteeMembership, Member
from schemas import CommitteeResponse, CommitteeMembershipResponse, MemberResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[CommitteeResponse])
async def get_committees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    chamber: Optional[str] = None,
    subcommittee: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get committees with optional filtering
    """
    query = db.query(Committee)
    
    # Apply filters
    if chamber:
        query = query.filter(Committee.chamber == chamber)
    if subcommittee is not None:
        query = query.filter(Committee.subcommittee == subcommittee)
    
    # Order by name
    committees = query.order_by(Committee.name).offset(skip).limit(limit).all()
    
    return committees

@router.get("/by-chamber/{chamber}", response_model=List[CommitteeResponse])
async def get_committees_by_chamber(
    chamber: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get committees by chamber
    """
    if chamber.lower() not in ['house', 'senate', 'joint']:
        raise HTTPException(status_code=400, detail="Chamber must be 'House', 'Senate', or 'Joint'")
    
    committees = db.query(Committee).filter(
        Committee.chamber == chamber.title()
    ).order_by(Committee.name).offset(skip).limit(limit).all()
    
    return committees

@router.get("/main", response_model=List[CommitteeResponse])
async def get_main_committees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    chamber: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get main committees (exclude subcommittees)
    """
    query = db.query(Committee).filter(Committee.subcommittee == False)
    
    if chamber:
        query = query.filter(Committee.chamber == chamber)
    
    committees = query.order_by(Committee.name).offset(skip).limit(limit).all()
    
    return committees

@router.get("/subcommittees", response_model=List[CommitteeResponse])
async def get_subcommittees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    parent_committee_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get subcommittees
    """
    query = db.query(Committee).filter(Committee.subcommittee == True)
    
    if parent_committee_id:
        query = query.filter(Committee.parent_committee_id == parent_committee_id)
    
    committees = query.order_by(Committee.name).offset(skip).limit(limit).all()
    
    return committees

@router.get("/{committee_id}", response_model=CommitteeResponse)
async def get_committee(committee_id: int, db: Session = Depends(get_db)):
    """
    Get a specific committee by ID
    """
    committee = db.query(Committee).filter(Committee.id == committee_id).first()
    
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    return committee

@router.get("/{committee_id}/members", response_model=List[MemberResponse])
async def get_committee_members(
    committee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get members of a specific committee
    """
    # Verify committee exists
    committee = db.query(Committee).filter(Committee.id == committee_id).first()
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    members = db.query(Member).join(CommitteeMembership).filter(
        CommitteeMembership.committee_id == committee_id
    ).order_by(Member.name).offset(skip).limit(limit).all()
    
    return members

@router.get("/{committee_id}/memberships", response_model=List[CommitteeMembershipResponse])
async def get_committee_memberships(
    committee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get committee memberships for a specific committee
    """
    # Verify committee exists
    committee = db.query(Committee).filter(Committee.id == committee_id).first()
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    memberships = db.query(CommitteeMembership).filter(
        CommitteeMembership.committee_id == committee_id
    ).order_by(CommitteeMembership.start_date.desc()).offset(skip).limit(limit).all()
    
    return memberships

@router.get("/member/{member_id}/committees", response_model=List[CommitteeResponse])
async def get_member_committees(
    member_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get committees for a specific member
    """
    # Verify member exists
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    committees = db.query(Committee).join(CommitteeMembership).filter(
        CommitteeMembership.member_id == member_id
    ).order_by(Committee.name).offset(skip).limit(limit).all()
    
    return committees
