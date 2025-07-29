# PV Forecast Comparison for Home Assistant

This system compares PV production forecasts with actual production data in Home Assistant. It stores forecast data at 4 AM, 11 AM, 3 PM, and 11 PM to track forecast accuracy and production patterns.

## Features

- **Home Assistant Add-on**: Easy one-click installation
- **Web Interface**: Built-in monitoring and manual data collection
- **REST API**: Integration endpoints for external systems
- **SQLite Database**: Reliable data storage with automatic backups
- **Scheduled Collection**: Automated data collection at configurable times
- **Real-time Monitoring**: Live status and data viewing

## Installation

### Quick Start (Recommended)

1. **Add Repository to Home Assistant:**
   ```
   https://github.com/your-username/pv-forecast-comparison-addon
   ```

2. **Install Add-on:**
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Search for "PV Forecast Comparison"
   - Click **Install**

3. **Configure:**
   - Set your **Home Assistant URL** and **Long-lived Access Token**
   - Click **Start**

4. **Access Web Interface:**
   - Click **Open Web UI** in the add-on page

### Manual Installation

See [ADDON_INSTALLATION.md](ADDON_INSTALLATION.md) for detailed installation instructions.

## Configuration

### Required Settings

1. **Home Assistant URL**: Usually `http://supervisor/core`
2. **Long-Lived Access Token**: Create this in your Home Assistant profile

### Optional Settings

- **Forecast Entities**: List of entities to try for PV forecast data
- **Production Entities**: List of entities to try for current PV production  
- **Daily Entities**: List of entities to try for daily PV production
- **Collection Times**: Customize when data is collected
- **Log Level**: Set logging verbosity

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

Access the web interface through the add-on page. Features include:

- **Manual Data Collection**: Buttons for each time slot
- **System Status**: Real-time status monitoring
- **Latest Data**: View collected data in JSON format
- **Auto-refresh**: Updates every 30 seconds

### REST API

The add-on provides these API endpoints:

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

Data is stored in a SQLite database with two main tables:

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

## Integration with Home Assistant

### REST Sensors

Add these to your `configuration.yaml`:

```yaml
sensor:
  - platform: rest
    name: "PV Forecast Data"
    resource: http://localhost:8123/api/data
    scan_interval: 300
    value_template: "{{ value }}"
    
  - platform: rest
    name: "PV Forecast Status"
    resource: http://localhost:8123/api/status
    scan_interval: 300
    value_template: "{{ value_json.online }}"
```

### Automations

```yaml
automation:
  - alias: "PV Forecast Manual Collection"
    trigger:
      - platform: event
        event_type: pv_forecast_manual_trigger
    action:
      - service: rest_command.pv_forecast_collect
        data:
          url: http://localhost:8123/api/collect
          method: POST
          payload: '{"time_slot": "{{ trigger.event.data.time_slot }}"}'
```

## Troubleshooting

### Common Issues

1. **Add-on won't start**: Check configuration and logs
2. **No data collected**: Verify entity names and access token
3. **Web interface not accessible**: Check port conflicts

### Logs

View logs in the add-on page or check `/data/pv_forecast.log` in the container.

### Manual Database Access

```bash
# Access the add-on container
docker exec -it addon_pv_forecast_comparison sh

# Query the database
sqlite3 /data/pv_forecast.db "SELECT * FROM pv_forecast ORDER BY date DESC LIMIT 10;"
```

## Maintenance

### Backup Data

```bash
# In SSH & Web Terminal
cp /data/pv_forecast.db /backup/pv_forecast.db.backup
```

### Clean Old Data

```bash
# Access the add-on container
docker exec -it addon_pv_forecast_comparison sh

# Clean old data
sqlite3 /data/pv_forecast.db "DELETE FROM pv_forecast WHERE date < date('now', '-30 days');"
```

## Support

If you encounter issues:

1. Check the add-on logs
2. Review the troubleshooting section
3. Check the GitHub repository for issues
4. Ask in the Home Assistant community forums

## License

This project is licensed under the MIT License. 