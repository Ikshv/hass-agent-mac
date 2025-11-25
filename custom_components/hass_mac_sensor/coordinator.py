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
        """Set up device registry and dynamically discover sensors from Mac app."""
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
        
        _LOGGER.debug(f"Device '{DEVICE_NAME}' created/found with ID: {device.id}")
        
        # Dynamically discover all sensors from the Mac app
        # Look for all sensor.* states that have the "source" attribute set to "hass_mac_sensor_agent"
        associated_count = 0
        discovered_sensors = []
        
        # Get all states that start with "sensor."
        all_states = self.hass.states.async_all()
        for state in all_states:
            if not state.entity_id.startswith("sensor."):
                continue
            
            # Check if this sensor has the source attribute indicating it's from our Mac app
            attributes = state.attributes
            source = attributes.get("source")
            unique_id = attributes.get("unique_id")
            
            if source == "hass_mac_sensor_agent" or (unique_id and unique_id.startswith("hass_mac_sensor_agent_")):
                discovered_sensors.append(state.entity_id)
                
                # Get or create entity registry entry
                entity = entity_registry.async_get(state.entity_id)
                if entity:
                    # Entity exists in registry
                    if entity.device_id != device.id:
                        entity_registry.async_update_entity(
                            state.entity_id,
                            device_id=device.id,
                        )
                        _LOGGER.info(f"Associated {state.entity_id} with device {device.id}")
                        associated_count += 1
                    else:
                        _LOGGER.debug(f"{state.entity_id} already associated with device")
                else:
                    # Entity doesn't exist in registry, create it
                    try:
                        # Extract sensor ID from unique_id or entity_id
                        sensor_id = unique_id.replace("hass_mac_sensor_agent_", "") if unique_id else state.entity_id.replace("sensor.", "")
                        
                        entity_registry.async_get_or_create(
                            "sensor",
                            DOMAIN,
                            unique_id if unique_id else f"{DOMAIN}_{sensor_id}",
                            suggested_object_id=sensor_id,
                            device_id=device.id,
                        )
                        _LOGGER.info(f"Created entity registry entry for {state.entity_id} and associated with device")
                        associated_count += 1
                    except Exception as e:
                        _LOGGER.warning(f"Failed to create entity registry entry for {state.entity_id}: {e}")
        
        if associated_count > 0:
            _LOGGER.info(f"Associated {associated_count} sensors with device '{DEVICE_NAME}': {', '.join(discovered_sensors)}")
        elif discovered_sensors:
            _LOGGER.debug(f"Found {len(discovered_sensors)} sensors but they were already associated")
        else:
            _LOGGER.debug(f"No sensors found from Mac app. Make sure the Mac app is running and sending sensor data.")

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
