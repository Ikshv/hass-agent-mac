# HASS Mac Sensor

A Home Assistant integration that groups sensors from the HASS Mac Sensor Agent macOS app under a single device named "hass-ma".

## Features

- Groups all Mac sensors under a single device
- Automatic sensor discovery and association
- Clean device organization in Home Assistant
- Works with the HASS Mac Sensor Agent macOS app

## Installation

### Via HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz) is installed
2. Go to HACS → Integrations
3. Click the three dots menu (top right) → Custom repositories
4. Add this repository URL and select "Integration" as the category
5. Click "Install" on the HASS Mac Sensor integration
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/hass_mac_sensor` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "HASS Mac Sensor" and add it

## Requirements

- Home Assistant 2023.1 or later
- HASS Mac Sensor Agent macOS app running and sending sensor data

## Usage

1. Install this integration in Home Assistant
2. Run the HASS Mac Sensor Agent app on your Mac
3. Configure the app with your Home Assistant URL and access token
4. Start sending sensors from the app
5. All sensors will automatically appear grouped under the "hass-ma" device

## Supported Sensors

- CPU Usage
- Memory Usage
- Disk Usage
- Battery Level
- Charging Status
- Active/Idle Status
- System Uptime
- Network Sent/Received

## Links

- [Mac App Repository](https://github.com/Ikshv/hass-agent-mac)
- [Report Issues](https://github.com/Ikshv/hass-agent-mac/issues)
