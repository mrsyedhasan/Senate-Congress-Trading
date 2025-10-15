"""
Script to add sample data for demonstration purposes
"""
import asyncio
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Member, Trade, Committee, CommitteeMembership
from datetime import datetime, timedelta
import random

# Create tables
Base.metadata.create_all(bind=engine)

def add_sample_data():
    db = SessionLocal()
    
    try:
        # Add sample members
        members_data = [
            {
                "name": "Nancy Pelosi",
                "chamber": "House",
                "state": "CA",
                "party": "Democrat",
                "district": "11",
                "office": "H-312",
                "phone": "(202) 225-4965",
                "email": "nancy.pelosi@mail.house.gov",
                "website": "https://pelosi.house.gov"
            },
            {
                "name": "Mitch McConnell",
                "chamber": "Senate",
                "state": "KY",
                "party": "Republican",
                "office": "S-230",
                "phone": "(202) 224-2541",
                "email": "mitch.mcconnell@senate.gov",
                "website": "https://www.mcconnell.senate.gov"
            },
            {
                "name": "Chuck Schumer",
                "chamber": "Senate",
                "state": "NY",
                "party": "Democrat",
                "office": "S-322",
                "phone": "(202) 224-6542",
                "email": "chuck.schumer@senate.gov",
                "website": "https://www.schumer.senate.gov"
            },
            {
                "name": "Kevin McCarthy",
                "chamber": "House",
                "state": "CA",
                "party": "Republican",
                "district": "20",
                "office": "H-2468",
                "phone": "(202) 225-2915",
                "email": "kevin.mccarthy@mail.house.gov",
                "website": "https://kevinmccarthy.house.gov"
            },
            {
                "name": "Elizabeth Warren",
                "chamber": "Senate",
                "state": "MA",
                "party": "Democrat",
                "office": "S-309",
                "phone": "(202) 224-4543",
                "email": "elizabeth.warren@senate.gov",
                "website": "https://www.warren.senate.gov"
            }
        ]
        
        members = []
        for member_data in members_data:
            member = Member(**member_data)
            db.add(member)
            db.flush()
            members.append(member)
        
        # Add sample committees
        committees_data = [
            {
                "name": "House Committee on Financial Services",
                "code": "HSBA",
                "chamber": "House",
                "subcommittee": False,
                "description": "Oversees the entire financial services industry"
            },
            {
                "name": "Senate Committee on Banking, Housing, and Urban Affairs",
                "code": "SSBK",
                "chamber": "Senate",
                "subcommittee": False,
                "description": "Oversees banking, housing, and urban affairs"
            },
            {
                "name": "House Committee on Energy and Commerce",
                "code": "HSIF",
                "chamber": "House",
                "subcommittee": False,
                "description": "Oversees telecommunications, consumer protection, food and drug safety"
            },
            {
                "name": "Senate Committee on Finance",
                "code": "SSFI",
                "chamber": "Senate",
                "subcommittee": False,
                "description": "Oversees taxation, revenue, and other financial matters"
            }
        ]
        
        committees = []
        for committee_data in committees_data:
            committee = Committee(**committee_data)
            db.add(committee)
            db.flush()
            committees.append(committee)
        
        # Add committee memberships
        committee_memberships = [
            {"member": members[0], "committee": committees[0], "position": "Member"},
            {"member": members[1], "committee": committees[1], "position": "Ranking Member"},
            {"member": members[2], "committee": committees[1], "position": "Chair"},
            {"member": members[3], "committee": committees[0], "position": "Member"},
            {"member": members[4], "committee": committees[3], "position": "Member"},
        ]
        
        for membership_data in committee_memberships:
            membership = CommitteeMembership(
                member_id=membership_data["member"].id,
                committee_id=membership_data["committee"].id,
                position=membership_data["position"],
                start_date=datetime.utcnow() - timedelta(days=365)
            )
            db.add(membership)
        
        # Add sample trades
        tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "META", "NFLX", "DIS", "V"]
        companies = {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc.",
            "TSLA": "Tesla Inc.",
            "AMZN": "Amazon.com Inc.",
            "NVDA": "NVIDIA Corporation",
            "META": "Meta Platforms Inc.",
            "NFLX": "Netflix Inc.",
            "DIS": "Walt Disney Company",
            "V": "Visa Inc."
        }
        
        transaction_types = ["Buy", "Sell", "Exchange"]
        
        # Generate trades for the last 6 months
        for i in range(50):
            member = random.choice(members)
            ticker = random.choice(tickers)
            transaction_type = random.choice(transaction_types)
            transaction_date = datetime.utcnow() - timedelta(days=random.randint(1, 180))
            
            # Generate amount ranges
            amount_min = random.randint(1000, 50000)
            amount_max = amount_min + random.randint(0, 10000)
            
            trade = Trade(
                member_id=member.id,
                ticker=ticker,
                company_name=companies[ticker],
                transaction_type=transaction_type,
                transaction_date=transaction_date,
                amount_min=amount_min,
                amount_max=amount_max,
                description=f"Periodic Transaction Report - {transaction_type} {ticker}",
                source="Sample Data",
                filing_date=transaction_date + timedelta(days=random.randint(1, 45))
            )
            db.add(trade)
        
        db.commit()
        print("Sample data added successfully!")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()
