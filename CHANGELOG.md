# Changelog

## [1.0.0] - 2024-01-01

### Added
- Initial release of PV Forecast Comparison add-on
- Web interface with real-time charts and statistics
- Automated data collection at configurable times (4am, 11am, 3pm, 11pm)
- Manual data collection through web interface
- Historical data analysis with 7-day charts
- SQLite database for reliable data storage
- REST API endpoints for integration
- Configurable entity mapping for forecast and production sensors
- Beautiful dashboard with accuracy metrics
- System status monitoring
- Logging and error handling

### Features
- Compare PV production forecasts with actual production data
- Track forecasting accuracy over time
- Identify patterns in solar production
- Monitor daily energy production vs forecasts
- Export data for further analysis
- Responsive web interface for mobile and desktop

### Technical Details
- Built with Python 3.9 and Alpine Linux
- Uses aiohttp for async web server
- SQLite database for data persistence
- Chart.js for interactive visualizations
- Home Assistant REST API integration
- Docker-based deployment 