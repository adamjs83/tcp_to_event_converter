# TCP to Event Converter

A Home Assistant custom integration that creates a TCP server to receive messages from external devices and converts them into Home Assistant events. This allows any device or application capable of TCP communication to trigger automations in Home Assistant.

## Features

- 🌐 Simple TCP server that listens on a configurable port
- 🔄 Converts incoming TCP messages into Home Assistant events
- ⚙️ Easy configuration through Home Assistant UI
- 🎯 Lightweight with no external dependencies
- 🛡️ Robust error handling and graceful shutdown
- 📝 Comprehensive logging for debugging

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer.git`
6. Select "Integration" as the category
7. Click "Add"
8. Find "TCP to Event Converter" in the integration list and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Download the latest release or clone this repository
2. Copy the `tcp_to_event_converter` directory to your Home Assistant `custom_components` directory:
   ```
   <config_dir>/custom_components/tcp_to_event_converter/
   ```
3. Restart Home Assistant

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"TCP to Event Converter"**
4. Configure the following settings:
   - **TCP Port**: The port number to listen on (default: `54321`)
   - **Event Type**: The name of the event to fire (default: `tcp_event`)

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `TCP Port` | Port number for the TCP server (1-65535) | `54321` |
| `Event Type` | Name of the event fired in Home Assistant | `tcp_event` |

## Usage

### Message Format

Send messages to the TCP server in the following format:

```
device_id:button_id:action_type
```

**Example:**
```
living_room:button_1:press
```

This will fire a Home Assistant event with the following data:

```yaml
event_type: tcp_event  # Or your configured event type
event_data:
  device_id: living_room
  button_id: button_1
  action: press
```

### Testing with netcat

You can test the integration using `netcat` from the command line:

```bash
echo "living_room:button_1:press" | nc <home_assistant_ip> 54321
```

### Testing with Python

```python
import socket

def send_tcp_event(device_id, button_id, action):
    message = f"{device_id}:{button_id}:{action}\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("192.168.1.100", 54321))  # Replace with your HA IP
        sock.sendall(message.encode('utf-8'))

# Example usage
send_tcp_event("living_room", "button_1", "press")
send_tcp_event("bedroom", "switch_2", "toggle")
```

## Automation Examples

### Basic Button Press

```yaml
automation:
  - alias: "Living Room Button Press"
    trigger:
      - platform: event
        event_type: tcp_event
        event_data:
          device_id: living_room
          button_id: button_1
          action: press
    action:
      - service: light.toggle
        target:
          entity_id: light.living_room
```

### Multiple Actions

```yaml
automation:
  - alias: "Bedroom Button Actions"
    trigger:
      - platform: event
        event_type: tcp_event
        event_data:
          device_id: bedroom
          button_id: button_1
    action:
      - choose:
          - conditions:
              - condition: template
                value_template: "{{ trigger.event.data.action == 'single_press' }}"
            sequence:
              - service: light.toggle
                target:
                  entity_id: light.bedroom

          - conditions:
              - condition: template
                value_template: "{{ trigger.event.data.action == 'double_press' }}"
            sequence:
              - service: scene.turn_on
                target:
                  entity_id: scene.bedroom_night

          - conditions:
              - condition: template
                value_template: "{{ trigger.event.data.action == 'long_press' }}"
            sequence:
              - service: light.turn_off
                target:
                  entity_id: all
```

### Generic Event Handler

```yaml
automation:
  - alias: "Log All TCP Events"
    trigger:
      - platform: event
        event_type: tcp_event
    action:
      - service: system_log.write
        data:
          message: >
            TCP Event: Device {{ trigger.event.data.device_id }},
            Button {{ trigger.event.data.button_id }},
            Action {{ trigger.event.data.action }}
          level: info
```

## Use Cases

- **ESP32/ESP8266 Projects**: Send button presses or sensor events to Home Assistant
- **Custom Hardware**: Integrate DIY devices without MQTT or HTTP overhead
- **Legacy Systems**: Connect older automation systems that support TCP
- **Rapid Prototyping**: Quick integration for testing without complex protocols
- **Crestron Systems**: Simple integration with Crestron home automation
- **Arduino Projects**: Easy communication from Arduino-based devices

## Troubleshooting

### Integration Won't Start

**Check the logs** (`Settings` → `System` → `Logs`):

- **"Address already in use"**: Another service is using the configured port. Change the port number or stop the conflicting service.
- **"Permission denied"**: Ports below 1024 require elevated permissions. Use a port above 1024.

### Events Not Firing

1. **Verify connection**: Use `netcat` or `telnet` to test connectivity:
   ```bash
   telnet <home_assistant_ip> 54321
   ```

2. **Check message format**: Ensure your message uses the correct format: `device_id:button_id:action`

3. **Enable debug logging** in `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.tcp_to_event_converter: debug
   ```

4. **Check Developer Tools**: Go to `Developer Tools` → `Events` and listen for your event type

### Firewall Issues

Ensure your firewall allows incoming TCP connections on the configured port:

```bash
# Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 54321 -j ACCEPT

# Linux (ufw)
sudo ufw allow 54321/tcp
```

### Connection Drops

- **Network stability**: Check for network issues or Wi-Fi problems
- **Timeout settings**: The server expects UTF-8 encoded messages
- **Multiple connections**: The server supports multiple simultaneous connections

## Security Considerations

⚠️ **Important Security Notes:**

1. **No Authentication**: This integration does not implement authentication. Any device that can reach the TCP port can send events.

2. **Network Exposure**: The server binds to `0.0.0.0`, accepting connections from all network interfaces.

3. **Recommendations**:
   - Run Home Assistant on a trusted network
   - Use firewall rules to restrict access to the TCP port
   - Consider using a VPN for remote access
   - Don't expose the port directly to the internet
   - Use non-standard ports to reduce automated scanning

## Technical Details

- **Protocol**: TCP
- **Encoding**: UTF-8
- **Port Range**: 1-65535 (configurable)
- **Concurrent Connections**: Unlimited (practical limits apply)
- **Message Format**: Simple colon-delimited strings
- **Dependencies**: None (uses Home Assistant's built-in asyncio)

## Changelog

### Version 1.0.1 (2025-11-10)
- Fixed critical shutdown timeout issue with active TCP connections
- Added proper task tracking and cancellation for client connections
- Improved error handling in setup and unload
- Added UnicodeDecodeError handling for non-UTF-8 data
- Made stop() method idempotent to prevent double-stop issues
- Removed redundant EVENT_HOMEASSISTANT_STOP listener
- Added comprehensive logging and debug messages
- Added type hints and constants for better code quality

### Version 1.0.0 (Initial Release)
- Initial release
- Basic TCP server functionality
- Config flow support
- Event firing on message receipt

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Clone the repository
2. Make your changes
3. Test thoroughly with Home Assistant
4. Submit a pull request

### Reporting Issues

Please report issues on the [GitHub Issues](https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer/issues) page with:
- Home Assistant version
- Integration version
- Detailed description of the issue
- Relevant logs

## License

This project is provided as-is without warranty. Feel free to use and modify for your needs.

## Credits

Created by adamjs83

## Support

For questions and support:
- Report issues: [Gitea Issues](https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer/issues)
- Home Assistant Community: [Community Forum](https://community.home-assistant.io/)

---

**Enjoy your TCP to Event Converter integration!** 🚀
