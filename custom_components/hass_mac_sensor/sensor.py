"""Sensor platform for HASS Mac Sensor."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEVICE_NAME
from .coordinator import HASSMacSensorCoordinator

# Sensor definitions
SENSOR_TYPES = {
    "cpu_usage": {
        "name": "CPU Usage",
        "unit": "%",
        "icon": "mdi:cpu-64-bit",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "memory_usage": {
        "name": "Memory Usage",
        "unit": "%",
        "icon": "mdi:memory",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "disk_usage": {
        "name": "Disk Usage",
        "unit": "%",
        "icon": "mdi:harddisk",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "battery_level": {
        "name": "Battery Level",
        "unit": "%",
        "device_class": SensorDeviceClass.BATTERY,
        "icon": "mdi:battery",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "is_charging": {
        "name": "Is Charging",
        "icon": "mdi:power-plug",
    },
    "is_active": {
        "name": "Is Active",
        "icon": "mdi:monitor",
    },
    "uptime": {
        "name": "Uptime",
        "unit": "h",
        "icon": "mdi:clock-outline",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "network_sent": {
        "name": "Network Sent",
        "unit": "MB",
        "icon": "mdi:upload",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "network_received": {
        "name": "Network Received",
        "unit": "MB",
        "icon": "mdi:download",
        "state_class": SensorStateClass.MEASUREMENT,
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HASS Mac Sensor sensors from a config entry."""
    coordinator: HASSMacSensorCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        HASSMacSensorEntity(coordinator, sensor_id, sensor_info)
        for sensor_id, sensor_info in SENSOR_TYPES.items()
    ]

    async_add_entities(entities)


class HASSMacSensorEntity(CoordinatorEntity, SensorEntity):
    """Representation of a HASS Mac Sensor sensor."""

    def __init__(
        self,
        coordinator: HASSMacSensorCoordinator,
        sensor_id: str,
        sensor_info: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._attr_name = sensor_info["name"]
        # Use the same entity_id format as the Mac app creates
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}"
        self._attr_device_info = coordinator.device_info
        # Use the same entity_id that the Mac app creates
        self.entity_id = f"sensor.{sensor_id}"

        if "unit" in sensor_info:
            self._attr_native_unit_of_measurement = sensor_info["unit"]
        if "device_class" in sensor_info:
            self._attr_device_class = sensor_info["device_class"]
        if "icon" in sensor_info:
            self._attr_icon = sensor_info["icon"]
        if "state_class" in sensor_info:
            self._attr_state_class = sensor_info["state_class"]

    @property
    def native_value(self) -> str | float | None:
        """Return the state of the sensor."""
        # The actual sensor values come from the Mac app via REST API
        # Read from the state that the Mac app creates
        state = self.hass.states.get(f"sensor.{self._sensor_id}")
        if state:
            try:
                return float(state.state)
            except (ValueError, TypeError):
                return state.state
        return None
