"""Config flow for HASS Mac Sensor."""
from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class HASSMacSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HASS Mac Sensor."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Check if already configured
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        # Create the config entry immediately
        # The Mac app sends data via REST API, so we don't need connection info
        # This integration just groups existing sensors under a device
        return self.async_create_entry(
            title="HASS Mac Sensor",
            data={},
        )
