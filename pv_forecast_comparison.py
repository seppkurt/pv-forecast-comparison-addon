#!/usr/bin/env python3
"""
PV Forecast Comparison Add-on
Compares PV production forecasts with actual production data.
"""

import os
import sys
import json
import sqlite3
import logging
import requests
from datetime import datetime, date
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/data/pv_forecast.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PVForecastComparison:
    """Main class for PV forecast comparison functionality."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the PV forecast comparison system."""
        self.config = config
        self.db_path = '/data/pv_forecast.db'
        self.ha_url = config.get('ha_url', 'http://supervisor/core')
        self.ha_token = config.get('ha_token', '')
        self.forecast_entities = config.get('forecast_entities', [])
        self.production_entities = config.get('production_entities', [])
        self.daily_entities = config.get('daily_entities', [])
        
        # Initialize database
        self.init_database()
        
    def init_database(self):
        """Initialize the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create pv_forecast table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pv_forecast (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    time_slot TEXT NOT NULL,
                    forecast_wh REAL,
                    actual_wh REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date, time_slot)
                )
            ''')
            
            # Create daily_production table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_production (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total_forecast_wh REAL,
                    total_actual_wh REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def get_ha_data(self, entity_id: str) -> Optional[float]:
        """Get data from Home Assistant API."""
        try:
            headers = {
                'Authorization': f'Bearer {self.ha_token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.ha_url}/api/states/{entity_id}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                state = data.get('state')
                if state and state != 'unavailable' and state != 'unknown':
                    try:
                        return float(state)
                    except (ValueError, TypeError):
                        logger.warning(f"Could not convert state '{state}' to float for {entity_id}")
                        return None
            else:
                logger.warning(f"Failed to get data for {entity_id}: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error getting data for {entity_id}: {e}")
            
        return None
    
    def get_forecast_data(self) -> Optional[float]:
        """Get PV forecast data from Home Assistant."""
        for entity in self.forecast_entities:
            value = self.get_ha_data(entity)
            if value is not None:
                logger.info(f"Found forecast data: {value}Wh from {entity}")
                return value
        
        logger.warning("No forecast data found from any configured entities")
        return None
    
    def get_production_data(self) -> Optional[float]:
        """Get current PV production data from Home Assistant."""
        for entity in self.production_entities:
            value = self.get_ha_data(entity)
            if value is not None:
                logger.info(f"Found production data: {value}Wh from {entity}")
                return value
        
        logger.warning("No production data found from any configured entities")
        return None
    
    def get_daily_pv_production(self) -> Optional[float]:
        """Get daily PV production data from Home Assistant."""
        for entity in self.daily_entities:
            value = self.get_ha_data(entity)
            if value is not None:
                logger.info(f"Found daily production data: {value}Wh from {entity}")
                return value
        
        logger.warning("No daily production data found from any configured entities")
        return None
    
    def store_forecast_data(self, time_slot: str, forecast_wh: float, actual_wh: float):
        """Store forecast and actual data in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = date.today().isoformat()
            
            cursor.execute('''
                INSERT OR REPLACE INTO pv_forecast 
                (date, time_slot, forecast_wh, actual_wh) 
                VALUES (?, ?, ?, ?)
            ''', (today, time_slot, forecast_wh, actual_wh))
            
            conn.commit()
            conn.close()
            logger.info(f"Stored data for {time_slot}: forecast={forecast_wh}Wh, actual={actual_wh}Wh")
            
        except Exception as e:
            logger.error(f"Error storing forecast data: {e}")
    
    def store_daily_production(self, forecast_wh: float, actual_wh: float):
        """Store daily production totals in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = date.today().isoformat()
            
            cursor.execute('''
                INSERT OR REPLACE INTO daily_production 
                (date, total_forecast_wh, total_actual_wh) 
                VALUES (?, ?, ?)
            ''', (today, forecast_wh, actual_wh))
            
            conn.commit()
            conn.close()
            logger.info(f"Stored daily production: forecast={forecast_wh}Wh, actual={actual_wh}Wh")
            
        except Exception as e:
            logger.error(f"Error storing daily production: {e}")
    
    def collect_data(self, time_slot: str):
        """Collect forecast and actual data for a specific time slot."""
        logger.info(f"Collecting data for time slot: {time_slot}")
        
        # Get forecast data
        forecast_wh = self.get_forecast_data()
        if forecast_wh is None:
            logger.error("Could not get forecast data")
            return False
        
        # Get actual production data
        actual_wh = self.get_production_data()
        if actual_wh is None:
            logger.warning("Could not get actual production data, using 0")
            actual_wh = 0
        
        # Store the data
        self.store_forecast_data(time_slot, forecast_wh, actual_wh)
        
        # For 11pm, store daily totals (complete day data)
        if time_slot == '11pm':
            daily_actual = self.get_daily_pv_production()
            if daily_actual is not None:
                logger.info(f"Daily production: {daily_actual}Wh")
                self.store_daily_production(forecast_wh, daily_actual)
        
        logger.info(f"Data collection completed for {time_slot}")
        return True 