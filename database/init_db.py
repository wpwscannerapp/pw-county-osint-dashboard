#!/usr/bin/env python3

import psycopg2
import os
from config import DATABASE_URL

def init_database():
    """Initialize the database with schema and initial data"""
    
    print("[*] Initializing PWC OSINT Dashboard Database...")
    
    schema = """
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    CREATE TABLE IF NOT EXISTS categories (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        description TEXT,
        color VARCHAR(10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS locations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        type VARCHAR(50),
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        radius_miles INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS sources (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        source_type VARCHAR(50),
        url VARCHAR(500),
        is_active BOOLEAN DEFAULT TRUE,
        last_fetch TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS incidents (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        title VARCHAR(500) NOT NULL,
        description TEXT,
        category VARCHAR(50) NOT NULL,
        incident_type VARCHAR(100),
        location VARCHAR(100),
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        source VARCHAR(100) NOT NULL,
        source_url VARCHAR(500),
        external_id VARCHAR(500) UNIQUE,
        sentiment DECIMAL(3, 2),
        is_critical BOOLEAN DEFAULT FALSE,
        is_duplicate BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deleted_at TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS alerts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        category VARCHAR(50),
        location VARCHAR(100),
        keywords TEXT[],
        alert_type VARCHAR(50),
        destination VARCHAR(500),
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS collection_logs (
        id SERIAL PRIMARY KEY,
        source_name VARCHAR(100),
        status VARCHAR(50),
        items_collected INT,
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX idx_incidents_created_at ON incidents(created_at DESC);
    CREATE INDEX idx_incidents_category ON incidents(category);
    CREATE INDEX idx_incidents_location ON incidents(location);
    CREATE INDEX idx_incidents_source ON incidents(source);
    
    INSERT INTO categories (name, description, color) VALUES
    ('police', 'Police incidents and arrests', '#FF6B6B'),
    ('fire', 'Fire department incidents', '#FFA500'),
    ('rescue', 'Rescue and EMS incidents', '#4ECDC4'),
    ('accident', 'Traffic accidents', '#FFD93D'),
    ('crime', 'Crime reports', '#CC0000'),
    ('emergency', 'Emergency situations', '#9B59B6'),
    ('news', 'Local news', '#3498DB')
    ON CONFLICT (name) DO NOTHING;
    
    INSERT INTO locations (name, type, latitude, longitude, radius_miles) VALUES
    ('Manassas', 'city', 38.7509, -77.4734, 5),
    ('Manassas Park', 'city', 38.7942, -77.4521, 3),
    ('Woodbridge', 'town', 38.6255, -77.2636, 8),
    ('Haymarket', 'town', 38.6431, -77.6314, 4),
    ('Triangle', 'town', 38.6147, -77.3264, 3),
    ('Dumfries', 'town', 38.5697, -77.3042, 5),
    ('Occoquan', 'town', 38.6835, -77.2825, 2),
    ('Prince William County', 'county', 38.6240, -77.4458, 25)
    ON CONFLICT (name) DO NOTHING;
    
    INSERT INTO sources (name, source_type, url, is_active) VALUES
    ('Prince William County Police Twitter', 'twitter', 'https://twitter.com/PWCPD', TRUE),
    ('Manassas City Police Twitter', 'twitter', 'https://twitter.com/ManassasCityPD', TRUE),
    ('Potomac Local News', 'rss', 'https://www.potomaclocal.com/feed/', TRUE),
    ('Bristow Beat', 'rss', 'https://www.bristowbeat.com/feed/', TRUE),
    ('Prince William Living', 'rss', 'https://princewilliamliving.com/feed/', TRUE),
    ('WTOP Prince William County', 'rss', 'https://wtop.com/local/prince-william-county/feed/', TRUE),
    ('Virginia Fire/EMS API', 'api', 'https://services.arcgisonline.com/arcgis/rest/services/Virginia_Fire_EMS/FeatureServer/0', TRUE)
    ON CONFLICT (name) DO NOTHING;
    """
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("[+] Connected to database")
        
        cursor.execute(schema)
        conn.commit()
        
        print("[+] Database schema created successfully")
        print("[+] Tables created: categories, locations, sources, incidents, alerts, collection_logs")
        print("[+] Initial data inserted")
        print("\n[✓] Database initialization complete!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"[!] Database error: {e}")
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    exit(0 if success else 1)
