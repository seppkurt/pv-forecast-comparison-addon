# Changelog

All notable changes to the PV Forecast Comparison Add-on will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of PV Forecast Comparison Add-on
- Automated data collection at 4 AM, 11 AM, 3 PM, and 11 PM
- Web interface for monitoring and manual data collection
- REST API endpoints for integration
- SQLite database for data storage
- Configurable entity names for different PV systems
- Real-time status monitoring
- Scheduled task management
- Logging and error handling

### Features
- **Data Collection**: Automatic collection of forecast and actual PV production data
- **Web UI**: Built-in interface for monitoring and manual operations
- **API**: REST endpoints for external integration
- **Database**: SQLite storage with automatic table creation
- **Configuration**: Easy setup through add-on options
- **Logging**: Comprehensive logging with configurable levels

### Technical Details
- Python 3.9+ based add-on
- aiohttp web framework
- SQLite database backend
- Docker containerization
- Multi-architecture support (armhf, armv7, aarch64, amd64, i386) 