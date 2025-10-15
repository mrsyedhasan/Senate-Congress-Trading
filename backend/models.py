from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    chamber = Column(String(10), nullable=False)  # "House" or "Senate"
    state = Column(String(2), nullable=False)
    party = Column(String(50))
    district = Column(String(10))  # For House members
    office = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trades = relationship("Trade", back_populates="member")
    committee_memberships = relationship("CommitteeMembership", back_populates="member")

class Committee(Base):
    __tablename__ = "committees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    chamber = Column(String(10), nullable=False)  # "House", "Senate", or "Joint"
    subcommittee = Column(Boolean, default=False)
    parent_committee_id = Column(Integer, ForeignKey("committees.id"))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    memberships = relationship("CommitteeMembership", back_populates="committee")
    parent = relationship("Committee", remote_side=[id])

class CommitteeMembership(Base):
    __tablename__ = "committee_memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    committee_id = Column(Integer, ForeignKey("committees.id"), nullable=False)
    position = Column(String(50))  # "Chair", "Ranking Member", "Member", etc.
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    member = relationship("Member", back_populates="committee_memberships")
    committee = relationship("Committee", back_populates="memberships")

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    ticker = Column(String(10), nullable=False, index=True)
    company_name = Column(String(255))
    transaction_type = Column(String(20), nullable=False)  # "Buy", "Sell", "Exchange"
    transaction_date = Column(DateTime, nullable=False, index=True)
    amount_min = Column(Float)  # Minimum transaction amount
    amount_max = Column(Float)  # Maximum transaction amount
    amount_exact = Column(Float)  # Exact amount if available
    
    # Exchange-specific fields
    exchange_from_ticker = Column(String(10))  # What was exchanged FROM
    exchange_from_company = Column(String(255))  # Company name of FROM asset
    exchange_from_amount = Column(Float)  # Amount of FROM asset
    exchange_ratio = Column(Float)  # Exchange ratio (TO amount / FROM amount)
    exchange_reason = Column(String(255))  # Reason for exchange
    
    description = Column(Text)
    source = Column(String(255))  # Source of the data
    filing_date = Column(DateTime)  # When the trade was filed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    member = relationship("Member", back_populates="trades")
