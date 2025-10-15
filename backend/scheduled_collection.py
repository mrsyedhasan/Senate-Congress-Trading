#!/usr/bin/env python3
"""
Scheduled data collection script
Can be run via cron job to automatically collect new data
"""
import asyncio
import sys
import os
from datetime import datetime
import logging

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from data_collector import collect_congress_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def scheduled_collection():
    """
    Run scheduled data collection
    """
    db = SessionLocal()
    
    try:
        logger.info("Starting scheduled data collection...")
        start_time = datetime.now()
        
        # Collect data from all sources
        await collect_congress_data(db)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"Scheduled collection completed in {duration:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Error during scheduled collection: {e}")
    finally:
        db.close()

def main():
    """
    Main function for scheduled collection
    """
    print(f"Scheduled data collection started at {datetime.now()}")
    asyncio.run(scheduled_collection())
    print(f"Scheduled data collection completed at {datetime.now()}")

if __name__ == "__main__":
    main()
