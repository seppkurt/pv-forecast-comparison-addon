# PV Forecast Comparison Add-on

A Home Assistant add-on that compares PV production forecasts with actual production data to help you monitor and improve your solar forecasting accuracy.

## Features

- **Real-time Comparison**: Compare forecasted vs actual PV production at different times of day
- **Historical Analysis**: View historical data to identify forecasting trends
- **Web Interface**: Beautiful web dashboard with charts and statistics
- **Automated Collection**: Scheduled data collection at configurable times (4am, 11am, 3pm, 11pm)
- **Manual Collection**: Trigger data collection manually through the web interface
- **Multiple Entity Support**: Configure multiple forecast and production entities

## Installation

1. Add this repository to your Home Assistant add-on store:
   ```
   https://github.com/seppkurt/pv-forecast-comparison-addon
   ```

2. Install the "PV Forecast Comparison" add-on from the add-on store

3. Configure the add-on with your Home Assistant URL and token

4. Start the add-on

## Configuration

### Required Configuration

- **ha_url**: Your Home Assistant URL (default: `http://supervisor/core`)
- **ha_token**: Your Home Assistant long-lived access token

### Optional Configuration

- **forecast_entities**: List of sensor entities that provide PV production forecasts
- **production_entities**: List of sensor entities that provide actual PV production data
- **daily_entities**: List of sensor entities that provide daily energy totals
- **collection_times**: Dictionary mapping time slots to collection times
- **log_level**: Logging level (INFO, DEBUG, WARNING, ERROR)

### Default Entity Names

The add-on is pre-configured to look for these common entity names:

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

Once the add-on is running, access the web interface at:
```
http://your-home-assistant-ip:8123
```

The web interface provides:
- **Dashboard**: Real-time comparison charts
- **Manual Collection**: Buttons to trigger data collection
- **Historical Data**: 7-day historical comparison charts
- **System Status**: Add-on status and database information

### Data Collection

The add-on automatically collects data at the following times:
- **4:00 AM**: Early morning forecast vs actual
- **11:00 AM**: Mid-morning comparison
- **3:00 PM**: Afternoon peak comparison
- **11:00 PM**: End-of-day summary

You can also manually trigger data collection through the web interface.

### Understanding the Data

- **Forecast vs Actual**: Compare predicted energy production with actual production
- **Accuracy Percentage**: Shows how accurate your forecasts are
- **Daily Totals**: Compare total daily forecast with actual daily production
- **Historical Trends**: View patterns over time to improve forecasting

## Troubleshooting

### Add-on Won't Start
- Check that `ha_url` and `ha_token` are properly configured
- Verify that your Home Assistant instance is accessible
- Check the add-on logs for error messages

### No Data Appearing
- Ensure your configured entities exist in Home Assistant
- Check that entities are providing numeric values
- Verify the entities are accessible with your token

### Web Interface Not Loading
- Ensure port 8123 is not being used by another service
- Check that the add-on is running and healthy
- Try refreshing the browser cache

## Support

For issues and feature requests, please visit:
- [GitHub Issues](https://github.com/seppkurt/pv-forecast-comparison-addon/issues)
- [Home Assistant Community](https://community.home-assistant.io/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 