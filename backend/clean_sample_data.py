#!/usr/bin/env python3
"""
Script to clean sample data from the database
This removes any trades that were generated as sample data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import Trade, Member, Committee, CommitteeMembership
from sqlalchemy import and_
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_sample_data():
    """
    Remove sample data from the database
    """
    db = next(get_db())
    
    try:
        # Remove trades with sample data sources
        sample_sources = [
            "Sample Data",
            "Realistic Trading Data", 
            "Senate Sample Data",
            "House Sample Data"
        ]
        
        sample_trades = db.query(Trade).filter(
            Trade.source.in_(sample_sources)
        ).all()
        
        logger.info(f"Found {len(sample_trades)} sample trades to remove")
        
        for trade in sample_trades:
            db.delete(trade)
        
        # Also remove trades with unrealistic descriptions
        sample_descriptions = db.query(Trade).filter(
            Trade.description.like("%sample%") |
            Trade.description.like("%realistic%") |
            Trade.description.like("%generated%")
        ).all()
        
        logger.info(f"Found {len(sample_descriptions)} trades with sample descriptions to remove")
        
        for trade in sample_descriptions:
            db.delete(trade)
        
        db.commit()
        logger.info("Sample data cleaned successfully!")
        
        # Show remaining data
        remaining_trades = db.query(Trade).count()
        remaining_members = db.query(Member).count()
        remaining_committees = db.query(Committee).count()
        
        logger.info(f"Remaining data:")
        logger.info(f"  - Trades: {remaining_trades}")
        logger.info(f"  - Members: {remaining_members}")
        logger.info(f"  - Committees: {remaining_committees}")
        
    except Exception as e:
        logger.error(f"Error cleaning sample data: {e}")
        db.rollback()

if __name__ == "__main__":
    clean_sample_data()
