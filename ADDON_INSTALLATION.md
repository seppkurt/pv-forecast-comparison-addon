# PV Forecast Comparison Add-on Installation Guide

This guide will help you install the PV Forecast Comparison add-on in your Home Assistant setup.

## Prerequisites

- Home Assistant with Supervisor (not Home Assistant Core)
- SSH & Web Terminal add-on installed (optional, for manual installation)
- Long-lived access token from Home Assistant

## Installation Methods

### Method 1: GitHub Repository (Recommended)

1. **Add the Repository**
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click the three dots (⋮) in the top right
   - Select **Repositories**
   - Add: `https://github.com/your-username/pv-forecast-comparison-addon`
   - Click **Add**

2. **Install the Add-on**
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Search for "PV Forecast Comparison"
   - Click on the add-on
   - Click **Install**

3. **Configure the Add-on**
   - After installation, click **Start**
   - Go to the **Configuration** tab
   - Set your **Home Assistant URL** (usually `http://supervisor/core`)
   - Add your **Long-lived Access Token**
   - Click **Save**

### Method 2: Manual Installation

1. **Download the Add-on Files**
   ```bash
   # In SSH & Web Terminal
   cd /addons
   git clone https://github.com/your-username/pv-forecast-comparison-addon
   ```

2. **Install via Supervisor**
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - The add-on should appear in the list
   - Click **Install**

### Method 3: Direct File Installation

1. **Create Add-on Directory**
   ```bash
   # In SSH & Web Terminal
   mkdir -p /addons/pv-forecast-comparison
   cd /addons/pv-forecast-comparison
   ```

2. **Copy Files**
   ```bash
   # Copy all files from the addon/ directory
   cp -r /path/to/your/addon/* .
   ```

3. **Install via Supervisor**
   - Restart the Supervisor
   - The add-on should appear in the Add-on Store

## Configuration

### Required Settings

1. **Home Assistant URL**
   - Usually: `http://supervisor/core`
   - If using external access: `http://your-ha-ip:8123`

2. **Long-Lived Access Token**
   - Go to your **Profile** in Home Assistant
   - Scroll down to **Long-Lived Access Tokens**
   - Click **Create Token**
   - Give it a name like "PV Forecast Comparison"
   - Copy the token and paste it in the add-on configuration

### Optional Settings

- **Forecast Entities**: List of entities to try for PV forecast data
- **Production Entities**: List of entities to try for current PV production
- **Daily Entities**: List of entities to try for daily PV production
- **Collection Times**: Customize when data is collected
- **Log Level**: Set logging verbosity

## Verification

### 1. Check Add-on Status
- Go to **Settings** → **Add-ons**
- Find "PV Forecast Comparison"
- Status should show "Running"

### 2. Access Web Interface
- Click on the add-on
- Click **Open Web UI**
- You should see the PV Forecast Comparison interface

### 3. Test Manual Collection
- In the web interface, click **Collect 4 AM Data**
- Check the **System Status** section
- Verify data appears in **Latest Data**

### 4. Check Logs
- In the add-on page, go to the **Logs** tab
- Look for successful data collection messages

## Troubleshooting

### Add-on Won't Start

1. **Check Configuration**
   - Verify Home Assistant URL is correct
   - Ensure long-lived access token is valid
   - Check that required fields are filled

2. **Check Logs**
   - Go to the add-on page
   - Click **Logs** tab
   - Look for error messages

3. **Common Issues**
   - **Port conflict**: Change port in configuration
   - **Permission issues**: Check file permissions
   - **Network issues**: Verify Home Assistant URL

### No Data Collected

1. **Verify Entity Names**
   - Check your PV entity names in Home Assistant
   - Go to **Developer Tools** → **States**
   - Search for your PV entities

2. **Test API Access**
   ```bash
   # In SSH & Web Terminal
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        -H "Content-Type: application/json" \
        "http://supervisor/core/api/states/sensor.your_pv_entity"
   ```

3. **Check Entity Availability**
   - Ensure your PV entities are not "unavailable"
   - Verify they have valid values

### Web Interface Not Accessible

1. **Check Port**
   - Verify port 8123 is not used by another add-on
   - Change port in configuration if needed

2. **Check Network**
   - Ensure add-on is running
   - Check firewall settings

3. **Access via IP**
   - Try accessing via IP address instead of hostname
   - Use: `http://your-ha-ip:8123`

## Integration with Home Assistant

### 1. Create Sensors
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

### 2. Create Automations
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

### 3. Create Dashboard
Use the dashboard configuration from the original files or create your own using the REST sensors.

## Maintenance

### Backup Data
```bash
# In SSH & Web Terminal
cp /data/pv_forecast.db /backup/pv_forecast.db.backup
```

### Update Add-on
- Go to the add-on page
- Click **Update** when available
- Restart the add-on after update

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

## Uninstallation

1. **Stop the Add-on**
   - Go to the add-on page
   - Click **Stop**

2. **Uninstall**
   - Click **Uninstall**
   - Confirm the action

3. **Clean Up (Optional)**
   ```bash
   # Remove data directory
   rm -rf /data/pv_forecast.db
   rm -rf /data/pv_forecast.log
   ``` 