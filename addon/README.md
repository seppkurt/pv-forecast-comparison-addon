# PV Forecast Comparison Add-on

A Home Assistant add-on that compares PV production forecasts with actual production data. It automatically collects data at 4 AM, 11 AM, 3 PM, and 11 PM to track forecast accuracy and production patterns.

## Features

- **Automated Data Collection**: Scheduled collection at 4 AM, 11 AM, 3 PM, and 11 PM
- **Web Interface**: Built-in web UI for monitoring and manual data collection
- **SQLite Database**: Reliable data storage with automatic backups
- **Configurable Entities**: Easy configuration of PV entity names
- **REST API**: API endpoints for integration with other systems
- **Real-time Monitoring**: Live status and data viewing

## Installation

### Method 1: Manual Installation

1. Download the add-on files to your Home Assistant `/addons` directory
2. Add the repository to your Home Assistant Supervisor
3. Install the add-on from the Add-on Store

### Method 2: Direct Repository

Add this repository to your Home Assistant Supervisor:

```
https://github.com/your-username/pv-forecast-comparison-addon
```

## Configuration

### Required Settings

1. **Home Assistant URL**: Usually `http://supervisor/core`
2. **Long-Lived Access Token**: Create this in your Home Assistant profile

### Optional Settings

- **Forecast Entities**: List of entities to try for PV forecast data
- **Production Entities**: List of entities to try for current PV production
- **Daily Entities**: List of entities to try for daily PV production
- **Collection Times**: Customize when data is collected
- **Log Level**: Set logging verbosity (DEBUG, INFO, WARNING, ERROR)

### Entity Configuration

The add-on will automatically try these common entity names:

**Forecast Entities:**
- `sensor.pv_production_forecast`
- `sensor.solar_forecast`
- `sensor.pv_forecast`
- `sensor.solar_production_forecast`

**Production Entities:**
- `sensor.pv_power`
- `sensor.solar_power`
- `sensor.pv_production`
- `sensor.solar_production`

**Daily Entities:**
- `sensor.pv_daily_energy`
- `sensor.solar_daily_energy`
- `sensor.pv_today_energy`
- `sensor.solar_today_energy`

## Usage

### Web Interface

Access the web interface at `http://your-ha-ip:8123` after installation. The interface provides:

- **Manual Data Collection**: Buttons to trigger data collection for each time slot
- **System Status**: Real-time status of the add-on
- **Latest Data**: View the most recent collected data

### API Endpoints

The add-on provides REST API endpoints:

- `GET /api/status` - Get system status
- `GET /api/data` - Get latest data
- `POST /api/collect` - Trigger manual data collection
- `GET /api/config` - Get current configuration

### Example API Usage

```bash
# Get system status
curl http://your-ha-ip:8123/api/status

# Trigger 11 AM data collection
curl -X POST http://your-ha-ip:8123/api/collect \
  -H "Content-Type: application/json" \
  -d '{"time_slot": "11am"}'

# Get latest data
curl http://your-ha-ip:8123/api/data
```

## Data Collection Schedule

- **4 AM**: Collects forecast data (no actual production yet)
- **11 AM**: Collects forecast + current production data
- **3 PM**: Collects forecast + current production data
- **11 PM**: Collects daily totals (complete day's production)

## Data Storage

Data is stored in a SQLite database at `/data/pv_forecast.db` with two main tables:

### pv_forecast table
- `id`: Primary key
- `date`: Date (YYYY-MM-DD)
- `time_slot`: Time slot (4am, 11am, 3pm, 11pm)
- `forecast_wh`: Forecasted production in Wh
- `actual_wh`: Actual production in Wh
- `timestamp`: When the data was stored

### daily_production table
- `id`: Primary key
- `date`: Date (YYYY-MM-DD)
- `total_forecast_wh`: Total forecasted production for the day
- `total_actual_wh`: Total actual production for the day
- `timestamp`: When the data was stored

## Troubleshooting

### Common Issues

1. **Add-on won't start**: Check the logs in the add-on page
2. **No data collected**: Verify your entity names and access token
3. **Web interface not accessible**: Check if port 8123 is available

### Logs

View logs in the add-on page or check `/data/pv_forecast.log` in the container.

### Manual Database Access

```bash
# Access the add-on container
docker exec -it addon_pv_forecast_comparison sh

# Query the database
sqlite3 /data/pv_forecast.db "SELECT * FROM pv_forecast ORDER BY date DESC LIMIT 10;"
```

## Development

### Building the Add-on

```bash
# Clone the repository
git clone https://github.com/your-username/pv-forecast-comparison-addon

# Build the add-on
docker build -t pv-forecast-comparison .

# Run locally for testing
docker run -p 8123:8123 -v /path/to/data:/data pv-forecast-comparison
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:

1. Check the logs in the add-on page
2. Review the troubleshooting section
3. Open an issue on GitHub
4. Check the Home Assistant community forums 