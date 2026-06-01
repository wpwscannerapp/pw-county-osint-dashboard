#!/usr/bin/env python3
import psycopg2
import logging
from config import DATABASE_URL, SCHEMA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    logger.info(f"🚀 Initializing Neon database - Schema: {SCHEMA}")
    
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=15)
        cur = conn.cursor()
        
        # Create schema
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};")
        cur.execute(f"SET search_path TO {SCHEMA};")
        
        # Main incidents table
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
        
        conn.commit()
        logger.info("✅ Neon database schema initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    init_database()
