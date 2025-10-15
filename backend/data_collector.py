"""
Data collection module for Congressional trading data from free sources
"""
import requests
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import logging

from models import Member, Trade, Committee, CommitteeMembership
from schemas import MemberCreate, TradeCreate, CommitteeCreate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CongressDataCollector:
    def __init__(self, db: Session):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Congressional Trading Dashboard (Educational Use)'
        })
    
    async def collect_senate_stock_data(self):
        """
        Collect data from Senate Stock Watcher GitHub repository
        """
        try:
            logger.info("Collecting Senate Stock Watcher data...")
            
            # GitHub API endpoint for the repository
            url = "https://api.github.com/repos/timothycarambat/senate-stock-watcher-data/contents/data"
            
            response = self.session.get(url)
            if response.status_code == 200:
                files = response.json()
                
                for file_info in files:
                    if file_info['name'].endswith('.json'):
                        await self._process_senate_file(file_info['download_url'])
            else:
                logger.warning(f"Failed to access Senate Stock Watcher data: {response.status_code}")
                        
        except Exception as e:
            logger.error(f"Error collecting Senate Stock Watcher data: {e}")
    
    async def _process_senate_file(self, download_url: str):
        """
        Process individual Senate stock data file
        """
        try:
            response = self.session.get(download_url)
            if response.status_code == 200:
                data = response.json()
                
                for trade_data in data:
                    await self._save_senate_trade(trade_data)
                    
        except Exception as e:
            logger.error(f"Error processing Senate file {download_url}: {e}")
    
    async def _save_senate_trade(self, trade_data: Dict):
        """
        Save individual Senate trade to database
        """
        try:
            # Extract member information
            senator_name = trade_data.get('senator', '')
            if not senator_name:
                return
                
            # Find or create member
            member = self.db.query(Member).filter(
                and_(
                    Member.name.ilike(f"%{senator_name}%"),
                    Member.chamber == "Senate"
                )
            ).first()
            
            if not member:
                # Create new Senate member
                member_data = MemberCreate(
                    name=senator_name,
                    chamber="Senate",
                    state=trade_data.get('state', ''),
                    party=trade_data.get('party', '')
                )
                member = Member(**member_data.dict())
                self.db.add(member)
                self.db.flush()
            
            # Create trade record
            trade_data_dict = {
                'member_id': member.id,
                'ticker': trade_data.get('ticker', ''),
                'company_name': trade_data.get('asset_description', ''),
                'transaction_type': trade_data.get('type', ''),
                'transaction_date': datetime.fromisoformat(trade_data.get('transaction_date', '').replace('Z', '+00:00')),
                'amount_min': self._parse_amount(trade_data.get('amount_min', '')),
                'amount_max': self._parse_amount(trade_data.get('amount_max', '')),
                'description': trade_data.get('description', ''),
                'source': 'Senate Stock Watcher',
                'filing_date': datetime.fromisoformat(trade_data.get('filing_date', '').replace('Z', '+00:00')) if trade_data.get('filing_date') else None
            }
            
            trade = Trade(**trade_data_dict)
            self.db.add(trade)
            
        except Exception as e:
            logger.error(f"Error saving Senate trade: {e}")
    
    def _parse_amount(self, amount_str: str) -> Optional[float]:
        """
        Parse amount string to float
        """
        if not amount_str:
            return None
        try:
            # Remove common prefixes and convert to float
            amount_str = amount_str.replace('$', '').replace(',', '')
            return float(amount_str)
        except:
            return None
    
    async def collect_house_trading_data(self):
        """
        Collect House trading data from various sources
        """
        try:
            logger.info("Collecting House trading data...")
            
            # Try to collect from CapitolGains package data
            await self._collect_capitol_gains_data()
            
            # Collect from other free sources
            await self._collect_stock_act_disclosures()
            
        except Exception as e:
            logger.error(f"Error collecting House trading data: {e}")
    
    async def _collect_capitol_gains_data(self):
        """
        Collect data using CapitolGains package approach
        """
        try:
            logger.info("Collecting CapitolGains data...")
            
            # TODO: Implement real CapitolGains data collection
            # In a real implementation, you would:
            # from capitolgains import CapitolGains
            # cg = CapitolGains()
            # data = cg.get_trades()
            
            logger.info("CapitolGains data collection not yet implemented - using real data sources only")
            
        except Exception as e:
            logger.error(f"Error collecting CapitolGains data: {e}")
    
    async def _collect_stock_act_disclosures(self):
        """
        Collect STOCK Act disclosure data
        """
        try:
            logger.info("Collecting STOCK Act disclosures...")
            
            # TODO: Implement real STOCK Act disclosure scraping
            # This would scrape official disclosure websites like:
            # - Senate.gov financial disclosure reports
            # - House.gov financial disclosure reports
            # - Clerk.house.gov disclosure reports
            
            logger.info("STOCK Act disclosure collection not yet implemented - using real data sources only")
            
        except Exception as e:
            logger.error(f"Error collecting STOCK Act disclosures: {e}")
    
    async def _add_realistic_trading_data(self):
        """
        DISABLED: Add realistic trading data based on known Congressional trading patterns
        This method is disabled to use only real data sources.
        """
        try:
            # DISABLED: This method generates sample data
            logger.info("Realistic trading data generation is disabled - using only real data sources")
            return
            
            # Realistic stock tickers that Congress members commonly trade
            realistic_tickers = [
                "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", 
                "DIS", "V", "MA", "JPM", "BAC", "WFC", "GS", "JNJ", "PFE", 
                "UNH", "HD", "PG", "KO", "PEP", "WMT", "TGT", "COST", "SBUX",
                "NKE", "ADBE", "CRM", "ORCL", "INTC", "AMD", "QCOM", "AVGO"
            ]
            
            companies = {
                "AAPL": "Apple Inc.", "MSFT": "Microsoft Corporation", "GOOGL": "Alphabet Inc.",
                "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Inc.", "NVDA": "NVIDIA Corporation",
                "META": "Meta Platforms Inc.", "NFLX": "Netflix Inc.", "DIS": "Walt Disney Company",
                "V": "Visa Inc.", "MA": "Mastercard Inc.", "JPM": "JPMorgan Chase & Co.",
                "BAC": "Bank of America Corp.", "WFC": "Wells Fargo & Company", "GS": "Goldman Sachs Group Inc.",
                "JNJ": "Johnson & Johnson", "PFE": "Pfizer Inc.", "UNH": "UnitedHealth Group Inc.",
                "HD": "Home Depot Inc.", "PG": "Procter & Gamble Co.", "KO": "Coca-Cola Company",
                "PEP": "PepsiCo Inc.", "WMT": "Walmart Inc.", "TGT": "Target Corporation",
                "COST": "Costco Wholesale Corporation", "SBUX": "Starbucks Corporation",
                "NKE": "Nike Inc.", "ADBE": "Adobe Inc.", "CRM": "Salesforce Inc.",
                "ORCL": "Oracle Corporation", "INTC": "Intel Corporation", "AMD": "Advanced Micro Devices Inc.",
                "QCOM": "QUALCOMM Incorporated", "AVGO": "Broadcom Inc."
            }
            
            # Generate realistic trades for the last 12 months
            from datetime import datetime, timedelta
            import random
            
            for i in range(100):  # Add 100 realistic trades
                member = random.choice(members)
                ticker = random.choice(realistic_tickers)
                transaction_type = random.choice(["Buy", "Sell", "Exchange"])
                
                # Generate realistic date (last 12 months)
                days_ago = random.randint(1, 365)
                transaction_date = datetime.utcnow() - timedelta(days=days_ago)
                
                # Generate realistic amounts (Congress members often trade in larger amounts)
                amount_min = random.randint(1000, 100000)
                
                # For Exchange transactions, add exchange-specific data
                exchange_from_ticker = None
                exchange_from_company = None
                exchange_from_amount = None
                exchange_ratio = None
                exchange_reason = None
                
                if transaction_type == "Exchange":
                    # Select a different ticker to exchange FROM
                    exchange_from_ticker = random.choice([t for t in realistic_tickers if t != ticker])
                    exchange_from_company = f"{exchange_from_ticker} Company"  # Simplified
                    exchange_from_amount = random.randint(1000, 100000)
                    exchange_ratio = round(amount_min / exchange_from_amount, 4)
                    exchange_reason = random.choice([
                        "Portfolio rebalancing",
                        "Sector rotation",
                        "Risk management",
                        "Tax optimization",
                        "Market outlook change"
                    ])
                amount_max = amount_min + random.randint(0, 50000)
                
                # Check if trade already exists
                existing_trade = self.db.query(Trade).filter(
                    Trade.member_id == member.id,
                    Trade.ticker == ticker,
                    Trade.transaction_date == transaction_date
                ).first()
                
                if not existing_trade:
                    trade = Trade(
                        member_id=member.id,
                        ticker=ticker,
                        company_name=companies.get(ticker, f"{ticker} Corporation"),
                        transaction_type=transaction_type,
                        transaction_date=transaction_date,
                        amount_min=amount_min,
                        amount_max=amount_max,
                        # Exchange-specific fields
                        exchange_from_ticker=exchange_from_ticker,
                        exchange_from_company=exchange_from_company,
                        exchange_from_amount=exchange_from_amount,
                        exchange_ratio=exchange_ratio,
                        exchange_reason=exchange_reason,
                        description=f"Periodic Transaction Report - {transaction_type} {ticker}" + 
                                  (f" FROM {exchange_from_ticker}" if exchange_from_ticker else ""),
                        source="Real Data Collection",
                        filing_date=transaction_date + timedelta(days=random.randint(1, 45))
                    )
                    self.db.add(trade)
            
            self.db.commit()
            logger.info("Added realistic trading data successfully")
            
        except Exception as e:
            logger.error(f"Error adding realistic trading data: {e}")
            self.db.rollback()

    async def collect_propublica_data(self, api_key: str):
        """
        Collect data from ProPublica Congress API
        """
        try:
            logger.info("Collecting ProPublica Congress data...")
            
            # Get current Congress members
            await self._collect_propublica_members(api_key)
            
            # Get committee data
            await self._collect_propublica_committees(api_key)
            
        except Exception as e:
            logger.error(f"Error collecting ProPublica data: {e}")
    
    async def _collect_propublica_members(self, api_key: str):
        """
        Collect member data from ProPublica
        """
        chambers = ['house', 'senate']
        
        for chamber in chambers:
            url = f"https://api.propublica.org/congress/v1/118/{chamber}/members.json"
            headers = {'X-API-Key': api_key}
            
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                for member_data in data['results'][0]['members']:
                    await self._save_propublica_member(member_data, chamber)
    
    async def _save_propublica_member(self, member_data: Dict, chamber: str):
        """
        Save ProPublica member data
        """
        try:
            # Check if member already exists
            existing_member = self.db.query(Member).filter(
                and_(
                    Member.name.ilike(f"%{member_data.get('first_name')}%{member_data.get('last_name')}%"),
                    Member.chamber == chamber.title()
                )
            ).first()
            
            if not existing_member:
                member_dict = {
                    'name': f"{member_data.get('first_name')} {member_data.get('last_name')}",
                    'chamber': chamber.title(),
                    'state': member_data.get('state', ''),
                    'party': member_data.get('party', ''),
                    'district': member_data.get('district') if chamber == 'house' else None,
                    'office': member_data.get('office', ''),
                    'phone': member_data.get('phone', ''),
                    'website': member_data.get('url', ''),
                }
                
                member = Member(**member_dict)
                self.db.add(member)
                self.db.flush()
                
        except Exception as e:
            logger.error(f"Error saving ProPublica member: {e}")
    
    async def _collect_propublica_committees(self, api_key: str):
        """
        Collect committee data from ProPublica
        """
        chambers = ['house', 'senate']
        
        for chamber in chambers:
            url = f"https://api.propublica.org/congress/v1/118/{chamber}/committees.json"
            headers = {'X-API-Key': api_key}
            
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                for committee_data in data['results'][0]['committees']:
                    await self._save_propublica_committee(committee_data, chamber)
    
    async def _save_propublica_committee(self, committee_data: Dict, chamber: str):
        """
        Save ProPublica committee data
        """
        try:
            # Check if committee already exists
            existing_committee = self.db.query(Committee).filter(
                Committee.code == committee_data.get('id', '')
            ).first()
            
            if not existing_committee:
                committee_dict = {
                    'name': committee_data.get('name', ''),
                    'code': committee_data.get('id', ''),
                    'chamber': chamber.title(),
                    'subcommittee': committee_data.get('subcommittee', False),
                    'description': committee_data.get('purpose', ''),
                }
                
                committee = Committee(**committee_dict)
                self.db.add(committee)
                
        except Exception as e:
            logger.error(f"Error saving ProPublica committee: {e}")

async def collect_congress_data(db: Session, propublica_api_key: Optional[str] = None):
    """
    Main function to collect all Congressional data
    """
    collector = CongressDataCollector(db)
    
    # Collect Senate Stock Watcher data (free)
    await collector.collect_senate_stock_data()
    
    # Collect House trading data (free)
    await collector.collect_house_trading_data()
    
    # Collect ProPublica data (free with API key)
    if propublica_api_key:
        await collector.collect_propublica_data(propublica_api_key)
    
    # Scrape real disclosure websites
    try:
        from real_data_scraper import scrape_real_data
        await scrape_real_data(db)
    except Exception as e:
        logger.error(f"Error scraping real data: {e}")
    
    # Commit all changes
    db.commit()
    logger.info("Data collection completed successfully")
