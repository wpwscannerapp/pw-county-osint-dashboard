# Prince William County OSINT Dashboard - Oracle Cloud Setup Guide

## Overview

This guide provides step-by-step instructions to deploy the PWC OSINT Dashboard on Oracle Cloud's Always Free tier.

## Prerequisites

- Oracle Cloud account (free tier)
- Linux Mint or Ubuntu 22.04+ machine locally (for development)
- SSH client
- Basic Linux knowledge

## Step 1: Create Oracle Cloud Account

1. Go to [oracle.com/cloud/free](https://www.oracle.com/cloud/free/)
2. Click "Start for free"
3. Sign up with email (NO credit card required for Always Free)
4. Verify email and complete account setup
5. Takes ~10-15 minutes

## Step 2: Create Compute Instance

In Oracle Cloud Console:

1. **Menu** → **Compute** → **Instances**
2. Click **Create Instance**
3. Configure:
   - **Name:** `pw-county-osint-dashboard`
   - **Image:** Ubuntu 22.04 LTS (always free eligible)
   - **Shape:** Always Free Eligible (ARM - Ampere A1)
     - Select 4 OCPUs / 24GB RAM
   - **VCN:** Create new or use default
   - **Subnet:** Public subnet
   - **Public IP:** Assign
   - **SSH Key:** Download and save private key
4. Click **Create**
5. Wait 2-3 minutes for instance to launch

## Step 3: Configure Firewall Rules

1. **Networking** → **Virtual Cloud Networks**
2. Select your VCN
3. **Security Lists** → Default security list
4. **Add Ingress Rule:**
   - **Protocol:** TCP
   - **Source:** 0.0.0.0/0
   - **Destination Port:** 8501 (Streamlit)
   - Click **Add Ingress Rule**

## Step 4: SSH Into Oracle Instance

From your Linux Mint terminal:

```bash
# Set permissions on SSH key
chmod 600 ~/Downloads/your-ssh-key.key

# SSH into your Oracle instance
ssh -i ~/Downloads/your-ssh-key.key ubuntu@YOUR-INSTANCE-IP-ADDRESS
```

Replace `YOUR-INSTANCE-IP-ADDRESS` with the public IP from Oracle Console.

## Step 5: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv git postgresql postgresql-contrib curl wget

# Create application directory
mkdir -p ~/pw-county-osint
cd ~/pw-county-osint
```

## Step 6: Clone Repository and Setup

```bash
# Clone the repository
git clone https://github.com/wpwscannerapp/pw-county-osint-dashboard.git
cd pw-county-osint-dashboard

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

## Step 7: Setup PostgreSQL Database

```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database user and database
sudo -u postgres psql << EOF
CREATE USER pwc_osint WITH PASSWORD 'your_secure_password';
CREATE DATABASE pwc_osint_db OWNER pwc_osint;
GRANT ALL PRIVILEGES ON DATABASE pwc_osint_db TO pwc_osint;
\q
EOF

# Initialize database schema
python database/init_db.py
```

## Step 8: Create Environment Configuration

```bash
# Create .env file
nano .env
```

Add:
```
DATABASE_URL=postgresql://pwc_osint:your_secure_password@localhost/pwc_osint_db
```

Save with Ctrl+X, then Y, then Enter.

## Step 9: Test Streamlit Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Run Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Check if it works (press Ctrl+C to stop):
```
You can now view your Streamlit app in your browser.
Network URL: http://YOUR-INSTANCE-IP:8501
```

## Step 10: Create Systemd Service for 24/7 Running

```bash
# Create service file
sudo nano /etc/systemd/system/pwc-osint.service
```

Paste:
```ini
[Unit]
Description=PWC OSINT Dashboard
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/pw-county-osint-dashboard
Environment="PATH=/home/ubuntu/pw-county-osint/venv/bin"
ExecStart=/home/ubuntu/pw-county-osint/venv/bin/python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --logger.level=info
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Save with Ctrl+X, Y, Enter.

## Step 11: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable pwc-osint.service

# Start the service
sudo systemctl start pwc-osint.service

# Check status
sudo systemctl status pwc-osint.service

# View logs
sudo journalctl -u pwc-osint.service -f
```

## Step 12: Access Your Dashboard

Open in browser:
```
http://YOUR-INSTANCE-IP:8501
```

Replace `YOUR-INSTANCE-IP` with the public IP from Oracle Cloud Console.

## Step 13 (Optional): Setup Free Domain

To make it easier to access instead of using IP:

1. Go to [duckdns.org](https://www.duckdns.org/)
2. Create account
3. Add new domain (e.g., `pwcosint`)
4. Get token
5. On Oracle instance:

```bash
# Install duckdns updater
sudo apt install duckdns -y

# Configure duckdns
sudo nano /etc/duckdns/duckdns.conf
```

Add your token and domain, then save.

Now access at: `http://pwcosint.duckdns.org:8501`

## Maintenance

### Check logs
```bash
sudo journalctl -u pwc-osint.service -f
```

### Stop/restart service
```bash
sudo systemctl stop pwc-osint.service
sudo systemctl restart pwc-osint.service
```

### Update code from GitHub
```bash
cd ~/pw-county-osint-dashboard
git pull origin main
sudo systemctl restart pwc-osint.service
```

### Restart data collectors
```bash
cd ~/pw-county-osint-dashboard
source venv/bin/activate
python scripts/run_collectors.py
```

## Troubleshooting

### Dashboard not loading
```bash
sudo systemctl status pwc-osint.service
sudo journalctl -u pwc-osint.service -n 50
```

### Database connection error
```bash
sudo -u postgres psql -c "SELECT version();"
psql -U pwc_osint -d pwc_osint_db -c "SELECT COUNT(*) FROM incidents;"
```

### Port 8501 already in use
```bash
sudo lsof -i :8501
sudo kill -9 <PID>
```

## Cost

- **Forever Free:** Oracle Cloud Always Free tier
  - 4 ARM vCPUs
  - 24GB RAM
  - 200GB storage
  - No billing after free trial
  - No credit card required

## Support

For issues or questions:
- Check logs: `sudo journalctl -u pwc-osint.service -f`
- GitHub Issues: https://github.com/wpwscannerapp/pw-county-osint-dashboard/issues
- Oracle Cloud Documentation: https://docs.oracle.com/

---

**Dashboard Status:** Running 24/7 on Oracle Cloud Always Free
**Last Updated:** May 2026
