"""Constants for the HASS Mac Sensor integration."""
from __future__ import annotations

DOMAIN = "hass_mac_sensor"

# Device identifiers
DEVICE_MANUFACTURER = "HASS Mac Sensor Agent"
DEVICE_MODEL = "Mac"
DEVICE_NAME = "hass-ma"

# Sensor update intervals (in seconds)
UPDATE_INTERVAL_CPU = 10
UPDATE_INTERVAL_MEMORY = 10
UPDATE_INTERVAL_DISK = 60
UPDATE_INTERVAL_BATTERY = 30
UPDATE_INTERVAL_ACTIVITY = 5
UPDATE_INTERVAL_UPTIME = 60
UPDATE_INTERVAL_NETWORK = 30
