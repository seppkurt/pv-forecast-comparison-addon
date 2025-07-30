#!/usr/bin/with-contenv bashio

# Load configuration
bashio::log.info "Starting PV Forecast Comparison Add-on"

# Check if configuration is valid
if ! bashio::config.has_value 'ha_url'; then
    bashio::log.error "ha_url is not set in configuration"
    exit 1
fi

if ! bashio::config.has_value 'ha_token'; then
    bashio::log.error "ha_token is not set in configuration"
    exit 1
fi

# Start the Python application
bashio::log.info "Starting PV Forecast Comparison application"
exec python3 /app/run.py 