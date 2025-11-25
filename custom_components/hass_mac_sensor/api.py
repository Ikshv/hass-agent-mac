"""API client for HASS Mac Sensor."""
from __future__ import annotations

import logging

_LOGGER = logging.getLogger(__name__)


class HASSMacSensorAPI:
    """API client for HASS Mac Sensor."""

    def __init__(self, host: str, token: str) -> None:
        """Initialize the API client."""
        self.host = host
        self.token = token
