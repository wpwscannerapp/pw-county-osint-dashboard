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
        self.schema = SCHEMA
        self.api_url = 'https://services.arcgisonline.com/arcgis/rest/services/Virginia_Fire_EMS/FeatureServer/0/query'
   
    def is_in_pwc(self, latitude, longitude):
        pwc_coords = (self.locations['Prince William County']['lat'],
                      self.locations['Prince William County']['lon'])
        distance = geodesic(pwc_coords, (latitude, longitude)).miles
        return distance <= self.locations['Prince William County']['radius_miles']
   
    def get_location_name(self, latitude, longitude):
        for location_name, data in self.locations.items():
            if location_name == 'Prince William County':
                continue
            distance = geodesic((data['lat'], data['lon']), (latitude, longitude)).miles
            if distance <= data['radius_miles']:
                return location_name
        return 'Prince William County'
   
    def store_incident(self, incident_data):
        try:
            # Use table with schema prefix
            response = self.supabase.table(f"{self.schema}.incidents").upsert(
                incident_data,
                on_conflict="external_id"
            ).execute()
            
            logger.info(f"[+] Stored Fire/EMS incident: {incident_data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"[!] Error storing Fire/EMS incident: {e}")
            return False
   
    def collect_incidents(self):
        logger.info("[*] Collecting Fire/EMS incidents...")
        
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
            
            count = 0
            for feature in data.get('features', []):
                attr = feature.get('attributes', {})
                geom = feature.get('geometry', {})
                
                if not geom.get('x') or not geom.get('y'):
                    continue
                    
                lat = geom['y']
                lon = geom['x']
                
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
                    "source_url": "",
                    "external_id": str(attr.get('OBJECTID', '')),
                    "created_at": datetime.now().isoformat()
                }
                
                if self.store_incident(incident):
                    count += 1
            
            logger.info(f"[+] Collected {count} Fire/EMS incidents")
            return count
            
        except Exception as e:
            logger.error(f"[!] Fire/EMS collection failed: {e}")
            return 0


def run_fire_ems_collector():
    collector = FireEMSCollector()
    collector.collect_incidents()


if __name__ == "__main__":
    run_fire_ems_collector()
