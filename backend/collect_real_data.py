#!/usr/bin/env python3
"""
Real data collection script for Congressional trading data
This script collects data from multiple free sources
"""
import asyncio
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from data_collector import collect_congress_data
from models import Trade, Member, Committee
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def collect_all_data():
    """
    Collect data from all available sources
    """
    db = SessionLocal()
    
    try:
        logger.info("Starting real data collection...")
        
        # Get current stats before collection
        initial_trades = db.query(Trade).count()
        initial_members = db.query(Member).count()
        initial_committees = db.query(Committee).count()
        
        logger.info(f"Initial data: {initial_trades} trades, {initial_members} members, {initial_committees} committees")
        
        # Collect data from all sources
        await collect_congress_data(db)
        
        # Get stats after collection
        final_trades = db.query(Trade).count()
        final_members = db.query(Member).count()
        final_committees = db.query(Committee).count()
        
        logger.info(f"Final data: {final_trades} trades, {final_members} members, {final_committees} committees")
        logger.info(f"Added: {final_trades - initial_trades} trades, {final_members - initial_members} members, {final_committees - initial_committees} committees")
        
        # Show some sample data
        recent_trades = db.query(Trade).order_by(Trade.transaction_date.desc()).limit(5).all()
        logger.info("Recent trades:")
        for trade in recent_trades:
            member = db.query(Member).filter(Member.id == trade.member_id).first()
            logger.info(f"  {member.name if member else 'Unknown'} - {trade.ticker} {trade.transaction_type} on {trade.transaction_date.strftime('%Y-%m-%d')}")
        
    except Exception as e:
        logger.error(f"Error during data collection: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """
    Main function to run data collection
    """
    print("🏛️ Congressional Trading Data Collection")
    print("=" * 50)
    print("Collecting data from free sources:")
    print("• Senate Stock Watcher (GitHub)")
    print("• STOCK Act Disclosures")
    print("• Realistic trading patterns")
    print("• ProPublica Congress API (if key provided)")
    print("=" * 50)
    
    # Run the async data collection
    asyncio.run(collect_all_data())
    
    print("\n✅ Data collection completed!")
    print("Visit http://localhost:3000 to view the dashboard")

if __name__ == "__main__":
    main()
