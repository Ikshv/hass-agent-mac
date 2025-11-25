"""DataUpdateCoordinator for HASS Mac Sensor."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEVICE_MANUFACTURER, DEVICE_MODEL, DEVICE_NAME
from .api import HASSMacSensorAPI

_LOGGER = logging.getLogger(__name__)


class HASSMacSensorCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the HASS Mac Sensor API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=5),
        )
        self.entry = entry
        self.api = HASSMacSensorAPI(
            entry.data.get("host", "http://localhost:8123"),
            entry.data.get("token", ""),
        )
        self._device_info: DeviceInfo | None = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        if self._device_info is None:
            self._device_info = DeviceInfo(
                identifiers={(DOMAIN, "hass_mac_sensor_agent")},
                manufacturer=DEVICE_MANUFACTURER,
                model=DEVICE_MODEL,
                name=DEVICE_NAME,
                sw_version="1.0.0",
            )
        return self._device_info

    async def async_setup_device_registry(self) -> None:
        """Set up device registry and associate existing sensors."""
        from homeassistant.helpers import device_registry as dr
        from homeassistant.helpers import entity_registry as er
        
        device_registry = dr.async_get(self.hass)
        entity_registry = er.async_get(self.hass)
        
        # Get or create device
        device = device_registry.async_get_or_create(
            config_entry_id=self.entry.entry_id,
            identifiers={(DOMAIN, "hass_mac_sensor_agent")},
            manufacturer=DEVICE_MANUFACTURER,
            model=DEVICE_MODEL,
            name=DEVICE_NAME,
            sw_version="1.0.0",
        )
        
        # Associate all sensor.* entities with this device
        sensor_ids = [
            "cpu_usage", "memory_usage", "disk_usage", "battery_level",
            "is_charging", "is_active", "uptime", "network_sent", "network_received"
        ]
        
        for sensor_id in sensor_ids:
            entity_id = f"sensor.{sensor_id}"
            entity = entity_registry.async_get(entity_id)
            if entity and entity.device_id != device.id:
                entity_registry.async_update_entity(
                    entity_id,
                    device_id=device.id,
                )

    async def _async_update_data(self) -> dict:
        """Fetch data from the HASS Mac Sensor API."""
        try:
            # The Mac app will send sensor data via REST API
            # This coordinator just provides device info for the sensors
            # The actual sensor updates come from the Mac app
            # Periodically check and associate new sensors with the device
            await self.async_setup_device_registry()
            return {}
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
