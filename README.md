# HASS Mac Sensor - Home Assistant Integration

A Home Assistant custom integration that groups sensors from the HASS Mac Sensor Agent macOS app under a single device named "hass-ma".

## Installation via HACS

1. Make sure [HACS](https://hacs.xyz) is installed in your Home Assistant instance
2. Go to **HACS → Integrations**
3. Click the **three dots menu** (top right) → **Custom repositories**
4. Add this repository:
   - **Repository**: `https://github.com/Ikshv/hass-agent-mac`
   - **Category**: Integration
5. Click **Install** on the HASS Mac Sensor integration
6. Restart Home Assistant
7. Go to **Settings → Devices & Services → Add Integration**
8. Search for **"HASS Mac Sensor"** and add it

## Manual Installation

1. Copy the `custom_components/hass_mac_sensor` folder to your Home Assistant `custom_components` directory:
   ```bash
   cp -r custom_components/hass_mac_sensor /config/custom_components/
   ```
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration**
4. Search for **"HASS Mac Sensor"** and add it

## Requirements

- Home Assistant 2023.1 or later
- HASS Mac Sensor Agent macOS app (see main repository)
- The Mac app must be running and sending sensor data

## How It Works

1. The Mac app sends sensor data via Home Assistant's REST API
2. This integration creates a device named "hass-ma" in Home Assistant
3. All sensors from the Mac app are automatically associated with this device
4. Sensors appear grouped under the device in Home Assistant's UI

## Supported Sensors

- CPU Usage (%)
- Memory Usage (%)
- Disk Usage (%)
- Battery Level (%)
- Charging Status (on/off)
- Active/Idle Status (on/off)
- System Uptime (hours)
- Network Sent/Received (MB)

## Configuration

The integration doesn't require any configuration - it automatically:
- Creates the "hass-ma" device
- Associates all sensors created by the Mac app with the device
- Updates device associations when new sensors are detected

## Troubleshooting

- **Device doesn't appear**: Make sure the Mac app is running and sending sensor data
- **Sensors not grouped**: Restart Home Assistant after installing the integration
- **Integration not found**: Make sure you've copied the files to `custom_components/hass_mac_sensor/`

## Links

- [Mac App Repository](https://github.com/Ikshv/hass-agent-mac)
- [Report Issues](https://github.com/Ikshv/hass-agent-mac/issues)
