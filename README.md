# Congressional Trading Dashboard

A comprehensive dashboard for tracking stock trades made by members of Congress and Senate, including committee memberships and transaction details.

## Features

- Real-time tracking of Congressional stock trades
- Committee membership information
- Transaction amounts and details
- Interactive data visualization
- Historical trading patterns
- Open-source data sources

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL with SQLAlchemy
- **Data Sources**: 
  - Senate Stock Watcher Data (GitHub)
  - CapitolGains Python Package
  - ProPublica Congress API
  - STOCK Act Disclosures
  - GovTrack API

## Data Sources

All data is sourced from free, publicly available, open-source repositories and APIs:

1. **Senate Stock Watcher Data**: Free JSON files of stock trades by U.S. Senators
   - GitHub: https://github.com/timothycarambat/senate-stock-watcher-data
2. **CapitolGains Python Package**: Free package for accessing Congressional financial disclosures
   - PyPI: https://pypi.org/project/capitolgains/
3. **ProPublica Congress API**: Free API for Congressional data and committee memberships
   - https://projects.propublica.org/api-docs/congress-api/
4. **STOCK Act Disclosures**: Official financial disclosures required by law
5. **GovTrack**: Free Congressional tracking and committee data
6. **OpenSecrets API**: Free political finance data (limited free tier)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd Senate-Congress-Trading

# Set up Python backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Set up React frontend
cd ../frontend
npm install
npm start
```

## Project Structure

```
├── backend/           # Python FastAPI backend
├── frontend/          # React TypeScript frontend
├── data/             # Data collection scripts
├── docs/             # Documentation
└── deployment/       # Docker and deployment configs
```

## Contributing

This project uses open-source data and is committed to transparency in government financial activities.
