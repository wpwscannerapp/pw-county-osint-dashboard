#!/usr/bin/env python3
"""
Database initialization script for PWC OSINT Dashboard
Uses the pwc_osint schema in Supabase
"""
import psycopg2
import logging
from config import DATABASE_URL, SCHEMA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    logger.info(f"Initializing database schema: {SCHEMA}")
    
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        cur = conn.cursor()
        
        # Set schema
        cur.execute(f"SET search_path TO {SCHEMA};")
        
        # Enable pgcrypto for UUIDs
        cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
        
        # Create tables
        cur.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insert default categories if table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL,
                color VARCHAR(10)
            );
        """)
        
        cur.execute("""
            INSERT INTO categories (name, color)
            VALUES 
                ('police', '#ef4444'),
                ('fire', '#f97316'),
                ('rescue', '#3b82f6'),
                ('news', '#64748b')
            ON CONFLICT (name) DO NOTHING;
        """)
        
        conn.commit()
        logger.info("✅ Database schema initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_database()
