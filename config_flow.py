"""Config flow for TCP to Event Converter integration."""

import asyncio
import logging
import re
import socket
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_TCP_PORT,
    CONF_EVENT_TYPE,
    MIN_PORT,
    MAX_PORT,
    EVENT_TYPE_PATTERN,
)

_LOGGER = logging.getLogger(__name__)


class TcpToEventConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TCP to Event Converter."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step of configuration.

        Args:
            user_input: User provided configuration data

        Returns:
            FlowResult with either form or entry creation
        """
        errors: Dict[str, str] = {}

        if user_input is not None:
            # Validate the configuration
            validation_error = await self._validate_config(user_input)

            if validation_error:
                errors["base"] = validation_error
            else:
                # Configuration is valid, create the entry
                return self.async_create_entry(
                    title=f"TCP Port {user_input[CONF_TCP_PORT]}",
                    data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_TCP_PORT, default=54321): int,
                vol.Required(CONF_EVENT_TYPE, default="tcp_event"): str,
            }),
            errors=errors,
        )

    async def _validate_config(self, config: Dict[str, Any]) -> Optional[str]:
        """Validate the user configuration.

        Performs comprehensive validation including:
        - Port range validation
        - Port availability check
        - Event type format validation
        - Duplicate entry detection

        Args:
            config: Configuration dictionary to validate

        Returns:
            Error code string if validation fails, None if valid
        """
        tcp_port = config[CONF_TCP_PORT]
        event_type = config[CONF_EVENT_TYPE]

        # 1. Validate port range
        if tcp_port < MIN_PORT:
            if tcp_port < 1024:
                _LOGGER.warning(
                    "Port %d is privileged (< 1024), requires root access", tcp_port
                )
                return "port_privileged"
            _LOGGER.error("Port %d is below minimum allowed port %d", tcp_port, MIN_PORT)
            return "invalid_port_range"

        if tcp_port > MAX_PORT:
            _LOGGER.error("Port %d exceeds maximum allowed port %d", tcp_port, MAX_PORT)
            return "invalid_port_range"

        # 2. Check for duplicate entries with same port
        for entry in self._async_current_entries():
            if entry.data.get(CONF_TCP_PORT) == tcp_port:
                _LOGGER.warning(
                    "Port %d is already configured in entry '%s'", tcp_port, entry.title
                )
                return "port_already_configured"

        # 3. Validate event type format
        if not self._validate_event_type(event_type):
            _LOGGER.error(
                "Invalid event type '%s': must start with letter, "
                "be lowercase, and contain only alphanumeric characters and underscores",
                event_type
            )
            return "invalid_event_type"

        # 4. Check if port is available by attempting to bind
        port_check_error = await self._check_port_available(tcp_port)
        if port_check_error:
            return port_check_error

        # All validations passed
        return None

    def _validate_event_type(self, event_type: str) -> bool:
        """Validate event type format.

        Event type must:
        - Start with a lowercase letter
        - Contain only lowercase letters, numbers, and underscores
        - Match pattern: ^[a-z][a-z0-9_]*$

        Args:
            event_type: The event type string to validate

        Returns:
            True if valid, False otherwise
        """
        if not event_type:
            return False

        pattern = re.compile(EVENT_TYPE_PATTERN)
        return bool(pattern.match(event_type))

    async def _check_port_available(self, port: int) -> Optional[str]:
        """Check if the specified port is available for binding.

        Attempts to temporarily bind to the port to verify availability.
        This prevents configuration errors that would only be discovered
        when the integration attempts to start the TCP server.

        Args:
            port: TCP port number to check

        Returns:
            Error code string if port check fails, None if available
        """
        try:
            # Create a socket and attempt to bind to the port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                # Attempt to bind to the port
                await asyncio.get_event_loop().run_in_executor(
                    None, sock.bind, ("0.0.0.0", port)
                )
                _LOGGER.debug("Port %d is available", port)
                return None

            except OSError as bind_error:
                if bind_error.errno == 98:  # Address already in use (Linux)
                    _LOGGER.error("Port %d is already in use", port)
                    return "port_in_use"
                elif bind_error.errno == 48:  # Address already in use (macOS)
                    _LOGGER.error("Port %d is already in use", port)
                    return "port_in_use"
                elif bind_error.errno == 13:  # Permission denied
                    _LOGGER.error("Permission denied to bind to port %d", port)
                    return "port_privileged"
                else:
                    _LOGGER.error(
                        "Cannot bind to port %d: %s (errno: %d)",
                        port, bind_error, bind_error.errno
                    )
                    return "cannot_bind"

            finally:
                # Always close the socket
                sock.close()

        except Exception as e:
            _LOGGER.error("Unexpected error checking port %d: %s", port, e)
            return "cannot_bind"

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for TCP to Event Converter."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow.

        Args:
            config_entry: The config entry being configured
        """
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options.

        Args:
            user_input: User provided options data

        Returns:
            FlowResult with either form or entry update
        """
        # Currently no options to configure, but structure is in place for future
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init")