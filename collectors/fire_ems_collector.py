#!/usr/bin/env python3
import logging
import requests
from datetime import datetime
from config import DATABASE_URL, PWC_LOCATIONS, SCHEMA
import psycopg2
from geopy.distance import geodesic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FireEMSCollector:
    def __init__(self):
        self.locations = PWC_LOCATIONS
        self.db_url = DATABASE_URL
        self.schema = SCHEMA
        self.conn = None
        self.api_url = 'https://services.arcgisonline.com/arcgis/rest/services/Virginia_Fire_EMS/FeatureServer/0/query'
   
    def connect_db(self):
        try:
            self.conn = psycopg2.connect(self.db_url, connect_timeout=10)
            logger.info("[+] Connected to Neon database")
        except Exception as e:
            logger.error(f"[!] Database connection failed: {e}")
            raise
   
    def close_db(self):
        if self.conn:
            self.conn.close()
   
    def is_in_pwc(self, latitude, longitude):
        pwc = self.locations['Prince William County']
        distance = geodesic((pwc['lat'], pwc['lon']), (latitude, longitude)).miles
        return distance <= pwc['radius_miles']
   
    def get_location_name(self, latitude, longitude):
        for name, data in self.locations.items():
            if name == 'Prince William County':
                continue
            distance = geodesic((data['lat'], data['lon']), (latitude, longitude)).miles
            if distance <= data['radius_miles']:
                return name
        return 'Prince William County'
   
    def store_incident(self, incident_data):
        try:
            cursor = self.conn.cursor()
            query = f"""
                INSERT INTO {self.schema}.incidents
                (title, description, category, incident_type, location,
                 latitude, longitude, source, source_url, external_id, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (external_id) DO NOTHING
            """
            cursor.execute(query, (
                incident_data.get('title', 'Fire/EMS Incident'),
                incident_data.get('description', ''),
                incident_data.get('category', 'fire'),
                incident_data.get('type', ''),
                incident_data.get('location', 'Prince William County'),
                incident_data.get('latitude'),
                incident_data.get('longitude'),
                'Virginia Fire/EMS API',
                incident_data.get('source_url', ''),
                incident_data.get('external_id', ''),
                datetime.now()
            ))
            self.conn.commit()
            cursor.close()
            logger.info(f"[+] Stored: {incident_data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"[!] Store error: {e}")
            return False

    def collect_incidents(self):
        logger.info("[*] Collecting Fire/EMS incidents...")
        try:
            params = {'where': '1=1', 'outFields': '*', 'returnGeometry': 'true', 'f': 'json', 'resultRecordCount': 1000}
            response = requests.get(self.api_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            count = 0
            for feature in data.get('features', []):
                attr = feature.get('attributes', {})
                geom = feature.get('geometry', {})
                if not geom.get('x') or not geom.get('y'):
                    continue

                lat, lon = geom['y'], geom['x']
                if not self.is_in_pwc(lat, lon):
                    continue

                incident = {
                    'title': attr.get('IncidentType', 'Fire/EMS Incident'),
                    'description': attr.get('Description', ''),
                    'category': 'fire',
                    'type': attr.get('IncidentType', ''),
                    'location': self.get_location_name(lat, lon),
                    'latitude': lat,
                    'longitude': lon,
                    'external_id': str(attr.get('OBJECTID', '')),
                }
                if self.store_incident(incident):
                    count += 1
            logger.info(f"[+] Collected {count} Fire/EMS incidents")
            return count
        except Exception as e:
            logger.error(f"[!] Collection error: {e}")
            return 0

    def collect_all(self):
        self.connect_db()
        try:
            self.collect_incidents()
        finally:
            self.close_db()

def run_fire_ems_collector():
    FireEMSCollector().collect_all()

if __name__ == "__main__":
    run_fire_ems_collector()
