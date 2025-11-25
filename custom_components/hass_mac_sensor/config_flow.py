"""Config flow for HASS Mac Sensor."""
from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

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

        if user_input is not None:
            # Create the config entry
            # The Mac app sends data via REST API, so we don't need connection info
            return self.async_create_entry(
                title="HASS Mac Sensor",
                data={},
            )

        # Show info form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description="This integration groups sensors from the HASS Mac Sensor Agent macOS app under a single device named 'hass-ma'. Make sure the Mac app is running and sending sensor data.",
        )
