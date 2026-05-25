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
            logger.info("[+] Connected to database")
        except Exception as e:
            logger.error(f"[!] Database connection failed: {e}")
            raise
   
    def close_db(self):
        if self.conn:
            self.conn.close()
            logger.info("[+] Database connection closed")
   
    def is_in_pwc(self, latitude, longitude):
        pwc_coords = (self.locations['Prince William County']['lat'],
                      self.locations['Prince William County']['lon'])
        incident_coords = (latitude, longitude)
       
        distance = geodesic(pwc_coords, incident_coords).miles
        radius = self.locations['Prince William County']['radius_miles']
       
        return distance <= radius
   
    def get_location_name(self, latitude, longitude):
        for location_name, location_data in self.locations.items():
            if location_name == 'Prince William County':
                continue
           
            location_coords = (location_data['lat'], location_data['lon'])
            incident_coords = (latitude, longitude)
           
            distance = geodesic(location_coords, incident_coords).miles
            if distance <= location_data['radius_miles']:
                return location_name
       
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
            logger.info(f"[+] Stored Fire/EMS incident: {incident_data.get('title', 'Unknown')}")
            return True
           
        except Exception as e:
            logger.error(f"[!] Error storing Fire/EMS incident: {e}")
            return False
   
    def collect_incidents(self):
        logger.info("[*] Collecting Fire/EMS incidents from Virginia API...")
       
        try:
            params = {
                'where': '1=1',
                'outFields': '*',
                'returnGeometry': 'true',
                'f': 'json',
                'resultRecordCount': 1000
            }
           
            response = requests.get(self.api_url, params=params, timeout=15)
            response.raise_for_status()
           
            data = response.json()
           
            if 'features' not in data:
                logger.warning("[!] No features in API response")
                return 0
           
            count = 0
            for feature in data['features']:
                attributes = feature.get('attributes', {})
                geometry = feature.get('geometry', {})
               
                if not geometry.get('x') or not geometry.get('y'):
                    continue
               
                latitude = geometry['y']
                longitude = geometry['x']
               
                if not self.is_in_pwc(latitude, longitude):
                    continue
               
                incident = {
                    'title': attributes.get('IncidentType', 'Fire/EMS Incident'),
                    'description': attributes.get('Description', ''),
                    'category': 'fire',
                    'type': attributes.get('IncidentType', ''),
                    'location': self.get_location_name(latitude, longitude),
                    'latitude': latitude,
                    'longitude': longitude,
                    'external_id': str(attributes.get('OBJECTID', '')),
                    'source_url': ''
                }
               
                if self.store_incident(incident):
                    count += 1
           
            logger.info(f"[+] Collected {count} Fire/EMS incidents in PWC")
            return count
           
        except Exception as e:
            logger.error(f"[!] Error collecting Fire/EMS incidents: {e}")
            return 0
   
    def collect_all(self):
        self.connect_db()
        try:
            self.collect_incidents()
        finally:
            self.close_db()


def run_fire_ems_collector():
    collector = FireEMSCollector()
    collector.collect_all()


if __name__ == "__main__":
    run_fire_ems_collector()
