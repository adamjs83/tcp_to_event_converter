# TCP to Event Converter - Home Assistant Custom Integration

## Project Overview

This is a Home Assistant custom integration that provides a TCP server to receive messages from external devices and convert them into Home Assistant events. The integration allows any device or application capable of TCP communication to trigger automations in Home Assistant.

**Domain:** `tcp_to_event_converter`
**Current Version:** 1.0.1
**Protocol:** TCP over IPv4
**Message Format:** `device_id:button_id:action_type` (colon-delimited)

## Architecture

### Core Components

1. **`__init__.py`** - Integration entry point
   - Handles async setup and teardown via config entries
   - Manages the TCPServer lifecycle
   - Implements `async_setup_entry()` and `async_unload_entry()`
   - Stores server instance in `hass.data[DOMAIN]`

2. **`tcp_server.py`** - TCP Server implementation
   - Asynchronous TCP server using `asyncio.start_server()`
   - Listens on `0.0.0.0` (all interfaces) on a configurable port
   - Tracks client connection tasks for proper cleanup
   - Parses incoming messages and fires Home Assistant events
   - Implements graceful shutdown with timeout handling

3. **`config_flow.py`** - Configuration UI flow
   - User-friendly config flow for setting up the integration
   - Validates TCP port (1-65535) and event type
   - Supports configuration through Home Assistant UI

4. **`const.py`** - Constants and configuration keys
   - `DOMAIN`: Integration domain identifier
   - `CONF_TCP_PORT`: TCP port configuration key
   - `CONF_EVENT_TYPE`: Event type configuration key

5. **`manifest.json`** - Integration metadata
   - Home Assistant integration manifest
   - Defines domain, name, version, and dependencies
   - Enables config flow support

## Key Design Patterns

### Async/Await

This integration is fully asynchronous and follows Home Assistant's async best practices:

- All I/O operations use `async`/`await`
- Uses `asyncio.start_server()` for the TCP server
- Connection handlers run as separate tasks
- Proper task tracking and cancellation on shutdown

### Error Handling

- Graceful handling of connection errors
- Unicode decode errors for non-UTF-8 data
- Timeout protection during shutdown (5 seconds)
- Idempotent `stop()` method to prevent double-stop issues
- Comprehensive exception logging with context

### Resource Management

- Active client connection tasks are tracked in a set
- Tasks are properly cancelled during shutdown
- Server closes new connections before waiting for existing ones
- Writer streams are properly closed in `finally` blocks
- Timeout protection prevents indefinite blocking

### Event Model

Messages received via TCP are parsed and fired as Home Assistant events:
```python
event_data = {
    "device_id": "living_room",
    "button_id": "button_1",
    "action": "press"
}
hass.bus.async_fire(event_type, event_data)
```

## Development Guidelines

### Home Assistant Integration Standards

1. **Config Entry Pattern**
   - Use config entries (not YAML configuration)
   - Implement `async_setup_entry()` and `async_unload_entry()`
   - Store integration data in `hass.data[DOMAIN]`

2. **Async Operations**
   - All setup/teardown must be async
   - Use `asyncio` for concurrent operations
   - Never block the event loop with synchronous I/O

3. **Logging**
   - Use module-level logger: `_LOGGER = logging.getLogger(__name__)`
   - Log levels: DEBUG (detailed), INFO (important events), WARNING (issues), ERROR (failures)
   - Include contextual information (ports, addresses, event data)

4. **Error Handling**
   - Return `False` from `async_setup_entry()` on setup failure
   - Return `False` from `async_unload_entry()` on cleanup failure
   - Log all exceptions with appropriate context
   - Handle `asyncio.CancelledError` by re-raising

5. **Type Hints**
   - Use type hints for all function signatures
   - Import from `typing` module (`Optional`, `Set`, etc.)
   - Helps with code maintainability and IDE support

### Coding Standards

1. **Python Style**
   - Follow PEP 8 style guidelines
   - Use 4 spaces for indentation
   - Maximum line length: 88 characters (Black formatter default)
   - Use double quotes for strings

2. **Naming Conventions**
   - Constants: `UPPER_CASE_WITH_UNDERSCORES`
   - Functions/methods: `snake_case`
   - Classes: `PascalCase`
   - Private methods: `_leading_underscore`

3. **Documentation**
   - Docstrings for all public functions and classes
   - Google-style docstrings preferred
   - Inline comments for complex logic

4. **Imports**
   - Standard library imports first
   - Third-party imports second
   - Local/relative imports last
   - Alphabetically sorted within each group

### Security Considerations

**CRITICAL:** This integration has security implications that must be understood:

1. **No Authentication**
   - The TCP server does NOT implement authentication
   - Any device that can reach the port can send events
   - This is a design trade-off for simplicity and compatibility

2. **Network Exposure**
   - Server binds to `0.0.0.0` (all network interfaces)
   - Accessible from LAN and potentially WAN if port forwarded
   - Could be exploited to trigger unwanted automations

3. **Input Validation**
   - Messages are validated for format (3 colon-separated parts)
   - Invalid messages are logged but do not crash the server
   - UTF-8 encoding is enforced (invalid data is skipped)

4. **Best Practices**
   - Document security considerations in README
   - Recommend firewall rules and network segmentation
   - Warn against direct internet exposure
   - Suggest VPN for remote access
   - Consider adding optional authentication in future versions

### Common Patterns

#### Starting the Server
```python
server = TCPServer(hass, tcp_port, event_type)
try:
    await server.start()
except Exception as e:
    _LOGGER.error("Failed to setup: %s", e)
    return False
```

#### Stopping the Server
```python
server = hass.data.pop(DOMAIN, None)
if server:
    try:
        await server.stop()
    except Exception as e:
        _LOGGER.error("Error stopping: %s", e)
        return False
```

#### Handling Connections
```python
async def handle_connection(self, reader, writer):
    addr = writer.get_extra_info("peername")
    try:
        # ... handle data ...
    except asyncio.CancelledError:
        raise  # Propagate cancellation
    except Exception as e:
        _LOGGER.error("Error: %s", e)
    finally:
        writer.close()
        await writer.wait_closed()
```

## Testing Considerations

### Manual Testing

1. **Netcat Testing**
   ```bash
   echo "device:button:action" | nc <ip> <port>
   ```

2. **Python Socket Testing**
   ```python
   import socket
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.connect(("192.168.1.100", 54321))
       s.sendall(b"test:button1:press\n")
   ```

3. **Event Monitoring**
   - Use Developer Tools > Events in Home Assistant
   - Listen for the configured event type
   - Verify event data matches expected format

### Test Scenarios

1. **Valid Messages**: Ensure proper event firing
2. **Invalid Format**: Verify logging and no crash
3. **Multiple Connections**: Test concurrent clients
4. **Connection Drops**: Ensure proper cleanup
5. **Invalid UTF-8**: Verify graceful handling
6. **Server Shutdown**: Confirm clean shutdown with active connections
7. **Port Conflicts**: Test error handling when port is in use
8. **Reload Integration**: Verify proper stop/start cycle

### Debug Logging

Enable debug logging in Home Assistant's `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.tcp_to_event_converter: debug
```

## File Structure

```
tcp_to_event_converter/
├── __init__.py           # Integration setup/teardown
├── tcp_server.py         # TCP server implementation
├── config_flow.py        # Configuration UI flow
├── const.py              # Constants and config keys
├── manifest.json         # Integration metadata
└── translations/         # UI translations
    └── en.json          # English translations
```

## Common Issues and Solutions

### "Address already in use"
- Another service is using the configured port
- Solution: Change port or stop conflicting service
- Check with: `lsof -i :<port>` or `netstat -an | grep <port>`

### "Permission denied"
- Trying to use privileged port (<1024)
- Solution: Use port >1024 or run with elevated privileges

### Shutdown timeout warnings
- Client connections not closing within 5 seconds
- Usually harmless but may indicate network issues
- Check for misbehaving clients or network problems

### Events not firing
- Check message format (must be 3 colon-separated parts)
- Verify TCP connection is established
- Enable debug logging to see received messages
- Check Home Assistant event bus with Developer Tools

## Future Enhancement Ideas

- Optional authentication (token-based)
- TLS/SSL support for encrypted connections
- Rate limiting to prevent abuse
- Configurable message format/parser
- WebSocket support alongside TCP
- Multiple concurrent integration instances (different ports)
- Connection statistics and monitoring
- IP whitelist/blacklist

## References

- [Home Assistant Integration Documentation](https://developers.home-assistant.io/docs/creating_integration_manifest)
- [Home Assistant Config Entries](https://developers.home-assistant.io/docs/config_entries_index)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Home Assistant Event Bus](https://www.home-assistant.io/docs/configuration/events/)

## Quick Start Checklist

When working on this integration:

- [ ] Understand the async/await patterns used throughout
- [ ] Review the shutdown flow and task cancellation logic
- [ ] Check security implications of any changes
- [ ] Test with multiple simultaneous connections
- [ ] Verify proper cleanup on integration reload
- [ ] Enable debug logging during development
- [ ] Test invalid input handling (malformed messages, bad UTF-8)
- [ ] Update version in manifest.json and README.md
- [ ] Document any new configuration options
- [ ] Update this system prompt if architecture changes
