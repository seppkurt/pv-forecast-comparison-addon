# PV Forecast Comparison Add-on Installation Guide

This guide will help you install and configure the PV Forecast Comparison add-on in Home Assistant.

## Prerequisites

- Home Assistant with Supervisor (not Home Assistant Core)
- A long-lived access token for Home Assistant
- PV production sensors in your Home Assistant instance

## Step 1: Add the Repository

1. Open your Home Assistant web interface
2. Go to **Settings** → **Add-ons**
3. Click on **Add-on Store** in the bottom right corner
4. Click the three dots menu (⋮) in the top right
5. Select **Repositories**
6. Click the **+** button to add a new repository
7. Enter the repository URL:
   ```
   https://github.com/seppkurt/pv-forecast-comparison-addon
   ```
8. Click **Add**

## Step 2: Install the Add-on

1. In the Add-on Store, you should now see a new section called **Local add-ons**
2. Find **PV Forecast Comparison** in the list
3. Click on the add-on to open its details page
4. Click **Install**
5. Wait for the installation to complete

## Step 3: Configure the Add-on

1. After installation, click **Configuration** tab
2. Configure the following settings:

### Required Settings

**Home Assistant URL:**
- Default: `http://supervisor/core`
- This should work for most installations

**Home Assistant Token:**
- Go to your Home Assistant profile page
- Scroll down to **Long-Lived Access Tokens**
- Click **Create Token**
- Give it a name like "PV Forecast Comparison"
- Copy the token and paste it in the add-on configuration

### Optional Settings

**Forecast Entities:**
- List of sensor entities that provide PV production forecasts
- Default entities are pre-configured for common names

**Production Entities:**
- List of sensor entities that provide actual PV production data
- Default entities are pre-configured for common names

**Daily Entities:**
- List of sensor entities that provide daily energy totals
- Default entities are pre-configured for common names

**Collection Times:**
- Dictionary mapping time slots to collection times
- Default: 4am, 11am, 3pm, 11pm

**Log Level:**
- Set to INFO for normal operation
- Set to DEBUG for troubleshooting

## Step 4: Start the Add-on

1. Click **Start** to launch the add-on
2. Check the **Logs** tab to ensure it started successfully
3. You should see messages indicating the add-on is running

## Step 5: Access the Web Interface

1. Once the add-on is running, click **Open Web UI**
2. Or navigate to: `http://your-home-assistant-ip:8123`
3. You should see the PV Forecast Comparison dashboard

## Step 6: Verify Data Collection

1. In the web interface, click one of the manual collection buttons
2. Check that data is being collected successfully
3. View the charts and statistics to verify everything is working

## Troubleshooting

### Add-on Won't Start
- Check the logs for error messages
- Verify your Home Assistant URL and token are correct
- Ensure your Home Assistant instance is accessible

### No Data in Charts
- Verify your entity names exist in Home Assistant
- Check that entities are providing numeric values
- Ensure your token has access to the configured entities

### Web Interface Not Loading
- Check that port 8123 is not being used by another service
- Try refreshing the browser cache
- Verify the add-on is running and healthy

### Common Entity Names

If you're not sure what entities to use, here are some common patterns:

**Forecast Entities:**
- `sensor.solar_forecast`
- `sensor.pv_production_forecast`
- `sensor.solar_production_forecast`

**Production Entities:**
- `sensor.solar_power`
- `sensor.pv_power`
- `sensor.solar_production`

**Daily Entities:**
- `sensor.solar_daily_energy`
- `sensor.pv_today_energy`
- `sensor.solar_today_energy`

## Getting Help

If you encounter issues:

1. Check the add-on logs for error messages
2. Verify your configuration settings
3. Test your Home Assistant token manually
4. Visit the [GitHub repository](https://github.com/seppkurt/pv-forecast-comparison-addon) for issues
5. Ask for help in the [Home Assistant Community](https://community.home-assistant.io/)

## Next Steps

Once the add-on is running:

1. **Monitor the data**: Check the web interface regularly to see forecast accuracy
2. **Adjust configuration**: Fine-tune entity names and collection times as needed
3. **Analyze trends**: Use the historical data to improve your forecasting
4. **Automate**: Set up automations based on forecast accuracy patterns 