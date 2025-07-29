#!/usr/bin/env python3
"""
PV Data Retriever
Retrieves data from the SQLite database for the web interface.
"""

import sqlite3
import json
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional

class PVDataRetriever:
    """Class for retrieving PV forecast data from the database."""
    
    def __init__(self, db_path: str):
        """Initialize the data retriever."""
        self.db_path = db_path
    
    def get_today_data(self) -> Dict[str, Any]:
        """Get today's data for all time slots."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = date.today().isoformat()
            
            # Get data for all time slots
            cursor.execute('''
                SELECT time_slot, forecast_wh, actual_wh 
                FROM pv_forecast 
                WHERE date = ?
                ORDER BY time_slot
            ''', (today,))
            
            result = {
                '4am': {'forecast': 0, 'actual': 0},
                '11am': {'forecast': 0, 'actual': 0},
                '3pm': {'forecast': 0, 'actual': 0},
                '11pm': {'forecast': 0, 'actual': 0},
                'daily': {'forecast': 0, 'actual': 0}
            }
            
            for row in cursor.fetchall():
                time_slot, forecast_wh, actual_wh = row
                if time_slot in result:
                    result[time_slot] = {
                        'forecast': forecast_wh or 0,
                        'actual': actual_wh or 0
                    }
            
            # Get daily totals
            cursor.execute('''
                SELECT total_forecast_wh, total_actual_wh 
                FROM daily_production 
                WHERE date = ?
            ''', (today,))
            
            daily_row = cursor.fetchone()
            if daily_row:
                total_forecast_wh, total_actual_wh = daily_row
                result['daily'] = {
                    'forecast': total_forecast_wh or 0,
                    'actual': total_actual_wh or 0
                }
            
            conn.close()
            return result
            
        except Exception as e:
            print(f"Error getting today's data: {e}")
            return {
                '4am': {'forecast': 0, 'actual': 0},
                '11am': {'forecast': 0, 'actual': 0},
                '3pm': {'forecast': 0, 'actual': 0},
                '11pm': {'forecast': 0, 'actual': 0},
                'daily': {'forecast': 0, 'actual': 0}
            }
    
    def get_historical_data(self, days: int = 7) -> Dict[str, Any]:
        """Get historical data for the specified number of days."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get dates for the last N days
            end_date = date.today()
            start_date = end_date - timedelta(days=days-1)
            
            # Get daily production data
            cursor.execute('''
                SELECT date, total_forecast_wh, total_actual_wh 
                FROM daily_production 
                WHERE date >= ? AND date <= ?
                ORDER BY date
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            dates = []
            forecast_data = []
            actual_data = []
            
            # Generate all dates in range
            current_date = start_date
            while current_date <= end_date:
                dates.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)
            
            # Fill in data from database
            db_data = {}
            for row in cursor.fetchall():
                db_date, forecast_wh, actual_wh = row
                db_data[db_date] = {
                    'forecast': forecast_wh or 0,
                    'actual': actual_wh or 0
                }
            
            # Create arrays with data (0 for missing dates)
            for date_str in dates:
                if date_str in db_data:
                    forecast_data.append(db_data[date_str]['forecast'])
                    actual_data.append(db_data[date_str]['actual'])
                else:
                    forecast_data.append(0)
                    actual_data.append(0)
            
            conn.close()
            
            return {
                'dates': dates,
                'forecast': forecast_data,
                'actual': actual_data
            }
            
        except Exception as e:
            print(f"Error getting historical data: {e}")
            return {
                'dates': [],
                'forecast': [],
                'actual': []
            }
    
    def get_db_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count records in pv_forecast table
            cursor.execute('SELECT COUNT(*) FROM pv_forecast')
            forecast_count = cursor.fetchone()[0]
            
            # Count records in daily_production table
            cursor.execute('SELECT COUNT(*) FROM daily_production')
            daily_count = cursor.fetchone()[0]
            
            # Get latest timestamp
            cursor.execute('''
                SELECT MAX(timestamp) FROM (
                    SELECT timestamp FROM pv_forecast
                    UNION ALL
                    SELECT timestamp FROM daily_production
                )
            ''')
            latest_timestamp = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'forecast_records': forecast_count,
                'daily_records': daily_count,
                'total_records': forecast_count + daily_count,
                'latest_timestamp': latest_timestamp
            }
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {
                'forecast_records': 0,
                'daily_records': 0,
                'total_records': 0,
                'latest_timestamp': None
            } 