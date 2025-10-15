from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MemberBase(BaseModel):
    name: str
    chamber: str  # "House" or "Senate"
    state: str
    party: Optional[str] = None
    district: Optional[str] = None
    office: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    bio: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class MemberResponse(MemberBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CommitteeBase(BaseModel):
    name: str
    code: str
    chamber: str  # "House", "Senate", or "Joint"
    subcommittee: bool = False
    parent_committee_id: Optional[int] = None
    description: Optional[str] = None

class CommitteeCreate(CommitteeBase):
    pass

class CommitteeResponse(CommitteeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CommitteeMembershipBase(BaseModel):
    member_id: int
    committee_id: int
    position: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CommitteeMembershipCreate(CommitteeMembershipBase):
    pass

class CommitteeMembershipResponse(CommitteeMembershipBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TradeBase(BaseModel):
    member_id: int
    ticker: str
    company_name: Optional[str] = None
    transaction_type: str  # "Buy", "Sell", "Exchange"
    transaction_date: datetime
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    amount_exact: Optional[float] = None
    
    # Exchange-specific fields
    exchange_from_ticker: Optional[str] = None
    exchange_from_company: Optional[str] = None
    exchange_from_amount: Optional[float] = None
    exchange_ratio: Optional[float] = None
    exchange_reason: Optional[str] = None
    
    description: Optional[str] = None
    source: Optional[str] = None
    filing_date: Optional[datetime] = None

class TradeCreate(TradeBase):
    pass

class TradeResponse(TradeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TradeWithMember(TradeResponse):
    member: MemberResponse

class MemberWithCommittees(MemberResponse):
    committees: List[CommitteeResponse] = []

class TradeWithMemberAndCommittees(TradeResponse):
    member: MemberWithCommittees

class DashboardStats(BaseModel):
    total_trades: int
    total_members: int
    total_committees: int
    recent_trades_count: int
    top_traded_stocks: List[dict]
    trades_by_chamber: dict
    trades_by_party: dict

class TradeFilter(BaseModel):
    member_id: Optional[int] = None
    chamber: Optional[str] = None
    party: Optional[str] = None
    ticker: Optional[str] = None
    transaction_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0
