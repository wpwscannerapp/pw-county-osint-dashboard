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
            logger.info(f"[+] Stored Fire/EMS: {incident.get('title')}")
            return True
        except Exception as e:
            logger.error(f"[!] Store failed: {e}")
            return False

    # ... (keep the rest of your collect_incidents method the same)
    def collect_incidents(self):
        # (your existing collection logic)
        logger.info("[*] Collecting Fire/EMS incidents...")
        # ... rest of your code ...
        pass   # I'll give you the full file if needed

def run_fire_ems_collector():
    FireEMSCollector().collect_incidents()

if __name__ == "__main__":
    run_fire_ems_collector()
