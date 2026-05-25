#!/usr/bin/env python3

import logging
import requests
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, PWC_LOCATIONS, SCHEMA
from supabase import create_client, Client
from geopy.distance import geodesic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FireEMSCollector:
    def __init__(self):
        self.locations = PWC_LOCATIONS
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = f"{SCHEMA}.incidents"
   
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
   
    def store_incident(self, incident):
        try:
            self.supabase.table(self.table_name).upsert(
                incident,
                on_conflict="external_id"
            ).execute()
            logger.info(f"[+] Stored: {incident.get('title')}")
            return True
        except Exception as e:
            logger.error(f"[!] Store failed: {e}")
            return False
   
    def collect_incidents(self):
        logger.info("[*] Collecting Fire/EMS incidents...")
        try:
            params = {
                'where': '1=1', 'outFields': '*', 'returnGeometry': 'true',
                'f': 'json', 'resultRecordCount': 1000
            }
            
            resp = requests.get(
                'https://services.arcgisonline.com/arcgis/rest/services/Virginia_Fire_EMS/FeatureServer/0/query',
                params=params, timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            
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
                    "title": attr.get('IncidentType', 'Fire/EMS Incident'),
                    "description": attr.get('Description', ''),
                    "category": "fire",
                    "incident_type": attr.get('IncidentType', ''),
                    "location": self.get_location_name(lat, lon),
                    "latitude": lat,
                    "longitude": lon,
                    "source": "Virginia Fire/EMS API",
                    "external_id": str(attr.get('OBJECTID', '')),
                    "created_at": datetime.now().isoformat()
                }
                
                if self.store_incident(incident):
                    count += 1
                    
            logger.info(f"[+] Collected {count} Fire/EMS incidents")
            
        except Exception as e:
            logger.error(f"Collection error: {e}")

def run_fire_ems_collector():
    FireEMSCollector().collect_incidents()

if __name__ == "__main__":
    run_fire_ems_collector()
