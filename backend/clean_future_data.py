#!/usr/bin/env python3
"""
Script to clean future dates and suspicious data from the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import Trade, Member, Committee, CommitteeMembership
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_future_and_suspicious_data():
    """
    Remove trades with future dates and suspicious sources
    """
    db = next(get_db())
    
    try:
        current_time = datetime.now()
        
        # Remove trades with future dates
        future_trades = db.query(Trade).filter(
            Trade.transaction_date > current_time
        ).all()
        
        logger.info(f"Found {len(future_trades)} trades with future dates to remove")
        
        for trade in future_trades:
            logger.info(f"Removing future trade: {trade.member.name} - {trade.ticker} {trade.transaction_type} on {trade.transaction_date}")
            db.delete(trade)
        
        # Remove trades from suspicious sources
        suspicious_sources = [
            "Senate Financial Disclosures",  # This was generating fake data
            "House Clerk Website",           # This was also generating fake data
            "Sample Data",
            "Realistic Trading Data"
        ]
        
        for source in suspicious_sources:
            source_trades = db.query(Trade).filter(Trade.source == source).all()
            if source_trades:
                logger.info(f"Removing {len(source_trades)} trades from suspicious source: {source}")
                for trade in source_trades:
                    db.delete(trade)
        
        # Remove trades with unrealistic descriptions
        fake_descriptions = db.query(Trade).filter(
            Trade.description.like("%Senate disclosure%") |
            Trade.description.like("%Scraped from House%") |
            Trade.description.like("%sample%") |
            Trade.description.like("%realistic%")
        ).all()
        
        if fake_descriptions:
            logger.info(f"Removing {len(fake_descriptions)} trades with fake descriptions")
            for trade in fake_descriptions:
                db.delete(trade)
        
        db.commit()
        logger.info("Suspicious data cleaned successfully!")
        
        # Show remaining data
        remaining_trades = db.query(Trade).count()
        remaining_members = db.query(Member).count()
        remaining_committees = db.query(Committee).count()
        
        logger.info(f"Remaining data:")
        logger.info(f"  - Trades: {remaining_trades}")
        logger.info(f"  - Members: {remaining_members}")
        logger.info(f"  - Committees: {remaining_committees}")
        
        # Show remaining sources
        remaining_sources = db.query(Trade.source).distinct().all()
        logger.info(f"Remaining data sources:")
        for source in remaining_sources:
            count = db.query(Trade).filter(Trade.source == source[0]).count()
            logger.info(f"  - {source[0]}: {count} trades")
        
    except Exception as e:
        logger.error(f"Error cleaning suspicious data: {e}")
        db.rollback()

if __name__ == "__main__":
    clean_future_and_suspicious_data()
