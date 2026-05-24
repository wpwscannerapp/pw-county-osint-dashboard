# Prince William County OSINT Dashboard

A real-time Open Source Intelligence (OSINT) dashboard for monitoring police, fire, rescue, and community incidents across Prince William County, Virginia and local municipalities.

## Coverage Areas

- Manassas
- Manassas Park
- Woodbridge
- Haymarket
- Triangle
- Dumfries
- Occoquan
- Unincorporated Prince William County

## Features

- ✅ Real-time incident monitoring
- ✅ Automated data collection (24/7)
- ✅ Location-based filtering
- ✅ Incident categorization (Police, Fire, Rescue)
- ✅ Sentiment analysis on social media
- ✅ Interactive Streamlit dashboard
- ✅ Community alerts system
- ✅ Incident heatmap visualization

## Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.10+
- **Database:** PostgreSQL
- **Hosting:** Oracle Cloud Always Free

## Quick Start

```bash
git clone https://github.com/wpwscannerapp/pw-county-osint-dashboard.git
cd pw-county-osint-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python database/init_db.py
streamlit run app.py
```

Dashboard available at: `http://localhost:8501`

## Oracle Cloud Deployment

See ORACLE_CLOUD_SETUP.md for complete deployment guide.

## Data Sources

**Police & Emergency:**
- Prince William County Police (@PWCPD)
- Manassas City Police (@ManassasCityPD)
- Virginia Fire/EMS API
- ArcGIS Crime Data

**Local News:**
- Potomac Local News
- Bristow Beat
- Prince William Living
- WTOP Prince William County

## License

GPL-3.0