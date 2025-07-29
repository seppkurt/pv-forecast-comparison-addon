#!/usr/bin/env python3
"""
PV Forecast Comparison Add-on Runner
Handles configuration and starts the services
"""

import os
import sys
import json
import logging
import asyncio
import aiohttp
from datetime import datetime
import yaml

# Add the app directory to Python path
sys.path.append('/app')

from pv_forecast_comparison import PVForecastComparison

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/data/pv_forecast.log')
    ]
)
logger = logging.getLogger(__name__)

class PVForecastAddon:
    def __init__(self):
        self.config = self.load_config()
        self.pv_comparison = None
        self.session = None
        
    def load_config(self):
        """Load configuration from add-on options."""
        config_path = '/data/options.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            return {
                'ha_url': 'http://supervisor/core',
                'ha_token': '',
                'forecast_entities': [
                    'sensor.pv_production_forecast',
                    'sensor.solar_forecast',
                    'sensor.pv_forecast',
                    'sensor.solar_production_forecast'
                ],
                'production_entities': [
                    'sensor.pv_power',
                    'sensor.solar_power',
                    'sensor.pv_production',
                    'sensor.solar_production'
                ],
                'daily_entities': [
                    'sensor.pv_daily_energy',
                    'sensor.solar_daily_energy',
                    'sensor.pv_today_energy',
                    'sensor.solar_today_energy'
                ],
                'collection_times': {
                    '4am': '04:00:00',
                    '11am': '11:00:00',
                    '3pm': '15:00:00',
                    '11pm': '23:00:00'
                },
                'log_level': 'INFO'
            }
    
    async def start(self):
        """Start the add-on services."""
        logger.info("Starting PV Forecast Comparison Add-on")
        
        # Set log level
        log_level = getattr(logging, self.config.get('log_level', 'INFO').upper())
        logging.getLogger().setLevel(log_level)
        
        # Initialize PV comparison
        self.pv_comparison = PVForecastComparison(
            ha_url=self.config['ha_url'],
            ha_token=self.config['ha_token'],
            db_path='/data/pv_forecast.db'
        )
        
        # Create aiohttp session
        self.session = aiohttp.ClientSession()
        
        # Start the web interface
        await self.start_web_interface()
        
        # Start scheduled tasks
        await self.start_scheduled_tasks()
        
        # Keep the add-on running
        while True:
            await asyncio.sleep(60)
    
    async def start_web_interface(self):
        """Start the web interface for configuration and monitoring."""
        from aiohttp import web
        
        app = web.Application()
        
        # API routes
        app.router.add_get('/', self.handle_home)
        app.router.add_get('/api/status', self.handle_status)
        app.router.add_get('/api/data', self.handle_data)
        app.router.add_get('/api/historical', self.handle_historical)
        app.router.add_post('/api/collect', self.handle_collect)
        app.router.add_get('/api/config', self.handle_config)
        
        # Static files
        app.router.add_static('/static', '/app/static')
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, '0.0.0.0', 8123)
        await site.start()
        
        logger.info("Web interface started on port 8123")
    
    async def handle_home(self, request):
        """Handle the home page."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>PV Forecast Comparison</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }
                .container { max-width: 1200px; margin: 0 auto; }
                .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
                .button:hover { background: #005a87; }
                .button:disabled { background: #ccc; cursor: not-allowed; }
                .status { padding: 15px; margin: 10px 0; border-radius: 5px; }
                .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
                .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
                .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
                .chart-container { position: relative; height: 400px; }
                .data-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
                .data-item { background: #f8f9fa; padding: 10px; border-radius: 5px; text-align: center; }
                .data-value { font-size: 1.5em; font-weight: bold; color: #007cba; }
                .data-label { font-size: 0.9em; color: #666; }
                .accuracy { font-size: 1.2em; font-weight: bold; }
                .accuracy.good { color: #28a745; }
                .accuracy.warning { color: #ffc107; }
                .accuracy.poor { color: #dc3545; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { color: #333; margin-bottom: 10px; }
                .header p { color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌞 PV Forecast Comparison</h1>
                    <p>Monitor and compare PV production forecasts with actual data</p>
                </div>
                
                <div class="card">
                    <h2>📊 Manual Data Collection</h2>
                    <button class="button" onclick="collectData('4am')" id="btn-4am">Collect 4 AM Data</button>
                    <button class="button" onclick="collectData('11am')" id="btn-11am">Collect 11 AM Data</button>
                    <button class="button" onclick="collectData('3pm')" id="btn-3pm">Collect 3 PM Data</button>
                    <button class="button" onclick="collectData('11pm')" id="btn-11pm">Collect 11 PM Data</button>
                </div>
                
                <div class="grid">
                    <div class="card">
                        <h2>📈 Today's Forecast vs Actual</h2>
                        <div class="chart-container">
                            <canvas id="todayChart"></canvas>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>📊 Daily Comparison</h2>
                        <div class="chart-container">
                            <canvas id="dailyChart"></canvas>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>📋 Today's Data Points</h2>
                    <div class="data-grid" id="dataGrid">
                        <!-- Data points will be populated here -->
                    </div>
                </div>
                
                <div class="card">
                    <h2>⚙️ System Status</h2>
                    <div id="status"></div>
                </div>
            </div>
            
            <script>
                let todayChart, dailyChart;
                
                async function collectData(timeSlot) {
                    const button = document.getElementById(`btn-${timeSlot}`);
                    button.disabled = true;
                    button.textContent = 'Collecting...';
                    
                    try {
                        const response = await fetch('/api/collect', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({time_slot: timeSlot})
                        });
                        const result = await response.json();
                        
                        if (result.success) {
                            showNotification('✅ ' + result.message, 'success');
                        } else {
                            showNotification('❌ ' + result.error, 'error');
                        }
                        
                        loadStatus();
                        loadData();
                        updateCharts();
                    } catch (error) {
                        showNotification('❌ Error: ' + error.message, 'error');
                    } finally {
                        button.disabled = false;
                        button.textContent = `Collect ${timeSlot.toUpperCase()} Data`;
                    }
                }
                
                function showNotification(message, type) {
                    const notification = document.createElement('div');
                    notification.className = `status ${type}`;
                    notification.textContent = message;
                    notification.style.position = 'fixed';
                    notification.style.top = '20px';
                    notification.style.right = '20px';
                    notification.style.zIndex = '1000';
                    document.body.appendChild(notification);
                    
                    setTimeout(() => {
                        notification.remove();
                    }, 3000);
                }
                
                async function loadStatus() {
                    try {
                        const response = await fetch('/api/status');
                        const status = await response.json();
                        document.getElementById('status').innerHTML = 
                            `<div class="status ${status.online ? 'success' : 'error'}">
                                <strong>Status:</strong> ${status.online ? '🟢 Online' : '🔴 Offline'}<br>
                                <strong>Last Update:</strong> ${status.last_update}<br>
                                <strong>Database Records:</strong> ${status.db_records}
                            </div>`;
                    } catch (error) {
                        document.getElementById('status').innerHTML = 
                            '<div class="status error">❌ Error loading status</div>';
                    }
                }
                
                async function loadData() {
                    try {
                        const response = await fetch('/api/data');
                        const data = await response.json();
                        updateDataGrid(data);
                    } catch (error) {
                        console.error('Error loading data:', error);
                    }
                }
                
                function updateDataGrid(data) {
                    const grid = document.getElementById('dataGrid');
                    const timeSlots = ['4am', '11am', '3pm', '11pm'];
                    
                    let html = '';
                    timeSlots.forEach(slot => {
                        const slotData = data[slot] || { forecast: 0, actual: 0 };
                        const forecast = slotData.forecast || 0;
                        const actual = slotData.actual || 0;
                        const accuracy = forecast > 0 ? ((actual / forecast) * 100).toFixed(1) : 0;
                        
                        html += `
                            <div class="data-item">
                                <div class="data-label">${slot.toUpperCase()}</div>
                                <div class="data-value">${forecast.toFixed(1)} Wh</div>
                                <div class="data-label">Forecast</div>
                                <div class="data-value">${actual.toFixed(1)} Wh</div>
                                <div class="data-label">Actual</div>
                                <div class="accuracy ${accuracy > 90 ? 'good' : accuracy > 70 ? 'warning' : 'poor'}">
                                    ${accuracy}% Accuracy
                                </div>
                            </div>
                        `;
                    });
                    
                    // Add daily totals
                    const dailyData = data.daily || { forecast: 0, actual: 0 };
                    const dailyForecast = dailyData.forecast || 0;
                    const dailyActual = dailyData.actual || 0;
                    const dailyAccuracy = dailyForecast > 0 ? ((dailyActual / dailyForecast) * 100).toFixed(1) : 0;
                    
                    html += `
                        <div class="data-item">
                            <div class="data-label">DAILY TOTAL</div>
                            <div class="data-value">${dailyForecast.toFixed(1)} Wh</div>
                            <div class="data-label">Forecast</div>
                            <div class="data-value">${dailyActual.toFixed(1)} Wh</div>
                            <div class="data-label">Actual</div>
                            <div class="accuracy ${dailyAccuracy > 90 ? 'good' : dailyAccuracy > 70 ? 'warning' : 'poor'}">
                                ${dailyAccuracy}% Accuracy
                            </div>
                        </div>
                    `;
                    
                    grid.innerHTML = html;
                }
                
                function updateCharts() {
                    updateTodayChart();
                    updateDailyChart();
                }
                
                async function updateTodayChart() {
                    try {
                        const response = await fetch('/api/data');
                        const data = await response.json();
                        
                        const timeSlots = ['4am', '11am', '3pm', '11pm'];
                        const forecastData = timeSlots.map(slot => data[slot]?.forecast || 0);
                        const actualData = timeSlots.map(slot => data[slot]?.actual || 0);
                        
                        if (todayChart) {
                            todayChart.destroy();
                        }
                        
                        const ctx = document.getElementById('todayChart').getContext('2d');
                        todayChart = new Chart(ctx, {
                            type: 'bar',
                            data: {
                                labels: timeSlots.map(slot => slot.toUpperCase()),
                                datasets: [{
                                    label: 'Forecast (Wh)',
                                    data: forecastData,
                                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                                    borderColor: 'rgba(54, 162, 235, 1)',
                                    borderWidth: 1
                                }, {
                                    label: 'Actual (Wh)',
                                    data: actualData,
                                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        title: {
                                            display: true,
                                            text: 'Energy (Wh)'
                                        }
                                    }
                                },
                                plugins: {
                                    title: {
                                        display: true,
                                        text: 'Today\'s Forecast vs Actual'
                                    }
                                }
                            }
                        });
                    } catch (error) {
                        console.error('Error updating today chart:', error);
                    }
                }
                
                async function updateDailyChart() {
                    try {
                        const response = await fetch('/api/historical?days=7');
                        const data = await response.json();
                        
                        if (dailyChart) {
                            dailyChart.destroy();
                        }
                        
                        const ctx = document.getElementById('dailyChart').getContext('2d');
                        dailyChart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: data.dates || [],
                                datasets: [{
                                    label: 'Daily Forecast (Wh)',
                                    data: data.forecast || [],
                                    borderColor: 'rgba(54, 162, 235, 1)',
                                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                                    tension: 0.1
                                }, {
                                    label: 'Daily Actual (Wh)',
                                    data: data.actual || [],
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                                    tension: 0.1
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        title: {
                                            display: true,
                                            text: 'Energy (Wh)'
                                        }
                                    }
                                },
                                plugins: {
                                    title: {
                                        display: true,
                                        text: '7-Day Historical Comparison'
                                    }
                                }
                            }
                        });
                    } catch (error) {
                        console.error('Error updating daily chart:', error);
                    }
                }
                
                // Load initial data
                loadStatus();
                loadData();
                updateCharts();
                
                // Refresh every 30 seconds
                setInterval(() => {
                    loadStatus();
                    loadData();
                    updateCharts();
                }, 30000);
            </script>
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')
    
    async def handle_status(self, request):
        """Handle status API request."""
        try:
            # Check if database exists and has data
            db_records = 0
            last_update = "Never"
            
            if os.path.exists('/data/pv_forecast.db'):
                import sqlite3
                conn = sqlite3.connect('/data/pv_forecast.db')
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM pv_forecast")
                db_records = cursor.fetchone()[0]
                cursor.execute("SELECT MAX(timestamp) FROM pv_forecast")
                result = cursor.fetchone()
                if result and result[0]:
                    last_update = result[0]
                conn.close()
            
            return web.json_response({
                'online': True,
                'last_update': last_update,
                'db_records': db_records
            })
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return web.json_response({
                'online': False,
                'error': str(e)
            })
    
    async def handle_data(self, request):
        """Handle data API request."""
        try:
            from pv_data_retriever import PVDataRetriever
            retriever = PVDataRetriever('/data/pv_forecast.db')
            data = retriever.get_today_data()
            return web.json_response(data)
        except Exception as e:
            logger.error(f"Error getting data: {e}")
            return web.json_response({'error': str(e)})
    
    async def handle_historical(self, request):
        """Handle historical data API request."""
        try:
            from pv_data_retriever import PVDataRetriever
            retriever = PVDataRetriever('/data/pv_forecast.db')
            
            # Get days parameter from query string
            days = int(request.query.get('days', 7))
            data = retriever.get_historical_data(days)
            return web.json_response(data)
        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            return web.json_response({'error': str(e)})
    
    async def handle_collect(self, request):
        """Handle manual data collection."""
        try:
            data = await request.json()
            time_slot = data.get('time_slot')
            
            if time_slot not in ['4am', '11am', '3pm', '11pm']:
                return web.json_response({'error': 'Invalid time slot'})
            
            # Run data collection
            self.pv_comparison.collect_data(time_slot)
            
            return web.json_response({
                'success': True,
                'message': f'Data collected for {time_slot}'
            })
        except Exception as e:
            logger.error(f"Error collecting data: {e}")
            return web.json_response({'error': str(e)})
    
    async def handle_config(self, request):
        """Handle configuration API request."""
        return web.json_response(self.config)
    
    async def start_scheduled_tasks(self):
        """Start scheduled data collection tasks."""
        logger.info("Starting scheduled tasks")
        
        # Schedule tasks for each collection time
        for time_slot, time_str in self.config['collection_times'].items():
            asyncio.create_task(self.schedule_task(time_slot, time_str))
    
    async def schedule_task(self, time_slot, time_str):
        """Schedule a task for a specific time."""
        while True:
            now = datetime.now()
            target_time = datetime.strptime(time_str, '%H:%M:%S').time()
            target_datetime = datetime.combine(now.date(), target_time)
            
            # If target time has passed today, schedule for tomorrow
            if target_datetime <= now:
                target_datetime = target_datetime.replace(day=target_datetime.day + 1)
            
            # Wait until target time
            wait_seconds = (target_datetime - now).total_seconds()
            logger.info(f"Scheduling {time_slot} collection for {target_datetime}")
            await asyncio.sleep(wait_seconds)
            
            # Execute collection
            try:
                logger.info(f"Executing scheduled collection for {time_slot}")
                self.pv_comparison.collect_data(time_slot)
            except Exception as e:
                logger.error(f"Error in scheduled collection for {time_slot}: {e}")

async def main():
    """Main function."""
    addon = PVForecastAddon()
    await addon.start()

if __name__ == "__main__":
    asyncio.run(main()) 