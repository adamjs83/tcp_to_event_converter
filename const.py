"""Constants for the TCP to Event Converter integration."""

# Integration domain and configuration keys
DOMAIN: str = "tcp_to_event_converter"
CONF_TCP_PORT: str = "tcp_port"
CONF_EVENT_TYPE: str = "event_type"

# Port validation constants
MIN_PORT: int = 1024  # Minimum port (avoid privileged ports)
MAX_PORT: int = 65535  # Maximum valid port number

# Message validation constants
EXPECTED_MESSAGE_PARTS: int = 3  # device_id:button_id:action
MAX_FIELD_LENGTH: int = 64  # Maximum characters per field
FIELD_VALIDATION_PATTERN: str = r"^[a-zA-Z0-9_-]+$"  # Alphanumeric, underscore, hyphen only

# Event type validation
EVENT_TYPE_PATTERN: str = r"^[a-z][a-z0-9_]*$"  # Must start with letter, lowercase alphanumeric + underscore

# Connection limits
MAX_CONNECTIONS: int = 100  # Maximum concurrent TCP connections

# Timeout constants
READ_TIMEOUT: float = 30.0  # Seconds to wait for read operations