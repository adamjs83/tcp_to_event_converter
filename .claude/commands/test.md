# Test TCP to Event Converter Integration

You are helping test the TCP to Event Converter Home Assistant custom integration. This command provides testing instructions and tools.

## Your Task

Provide comprehensive testing guidance and help the user test the TCP server functionality.

## Testing Methods

### 1. Using netcat (nc)

The simplest way to test is with netcat:

```bash
# Send a single message
echo "living_room:button_1:press" | nc <HOME_ASSISTANT_IP> <PORT>

# Interactive mode (type messages and press Enter)
nc <HOME_ASSISTANT_IP> <PORT>
# Then type: bedroom:switch_2:toggle
# Press Ctrl+C to exit

# Test from localhost if HA is local
echo "test:button1:single_press" | nc localhost 54321
```

### 2. Using Python Socket

Create a test script:

```python
#!/usr/bin/env python3
import socket
import sys

def send_tcp_event(host, port, device_id, button_id, action):
    """Send a TCP event to Home Assistant."""
    message = f"{device_id}:{button_id}:{action}\n"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((host, port))
            sock.sendall(message.encode('utf-8'))
            print(f"Sent: {message.strip()}")
    except ConnectionRefusedError:
        print(f"ERROR: Connection refused. Is the server running on {host}:{port}?")
    except socket.timeout:
        print(f"ERROR: Connection timeout to {host}:{port}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Configuration
    HOST = "192.168.1.100"  # Replace with your Home Assistant IP
    PORT = 54321            # Replace with your configured port

    # Test cases
    send_tcp_event(HOST, PORT, "living_room", "button_1", "press")
    send_tcp_event(HOST, PORT, "bedroom", "switch_2", "toggle")
    send_tcp_event(HOST, PORT, "kitchen", "sensor_3", "motion_detected")
```

### 3. Using telnet

```bash
# Connect interactively
telnet <HOME_ASSISTANT_IP> <PORT>

# Then type messages:
test:button1:press
living_room:switch1:toggle

# Press Ctrl+] then type 'quit' to exit
```

### 4. Testing Invalid Input

Test error handling:

```bash
# Invalid format (too few parts)
echo "invalid:message" | nc localhost 54321

# Invalid format (too many parts)
echo "too:many:parts:here:invalid" | nc localhost 54321

# Invalid UTF-8 (if your shell supports it)
echo -e "\xff\xfe\invalid" | nc localhost 54321

# Empty message
echo "" | nc localhost 54321
```

## Test Scenarios Checklist

### Basic Functionality
- [ ] Valid message fires event correctly
- [ ] Event appears in Developer Tools > Events
- [ ] Event data contains correct device_id, button_id, and action
- [ ] Multiple messages in sequence work

### Concurrent Connections
- [ ] Multiple simultaneous connections work
- [ ] Messages from different clients are processed
- [ ] No connection is blocked by another

### Error Handling
- [ ] Invalid format is logged but doesn't crash server
- [ ] Non-UTF-8 data is handled gracefully
- [ ] Connection drops are logged properly

### Integration Lifecycle
- [ ] Integration starts successfully
- [ ] Server listens on configured port
- [ ] Integration reload works correctly
- [ ] Integration unload cleans up properly
- [ ] No "Address already in use" after reload

### Network Tests
- [ ] Server accepts connections from LAN
- [ ] Firewall allows configured port (if applicable)
- [ ] Connection timeout handling works

## Monitoring Events in Home Assistant

### Using Developer Tools

1. Navigate to **Developer Tools** > **Events**
2. In "Listen to events" field, enter your event type (default: `tcp_event`)
3. Click **Start Listening**
4. Send test messages via TCP
5. Events should appear in real-time

### Using Automation for Testing

Create a test automation:

```yaml
automation:
  - alias: "TCP Event Logger"
    trigger:
      - platform: event
        event_type: tcp_event  # Use your configured event type
    action:
      - service: persistent_notification.create
        data:
          title: "TCP Event Received"
          message: >
            Device: {{ trigger.event.data.device_id }}
            Button: {{ trigger.event.data.button_id }}
            Action: {{ trigger.event.data.action }}
      - service: system_log.write
        data:
          message: "TCP Event: {{ trigger.event.data }}"
          level: info
```

## Checking Logs

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.tcp_to_event_converter: debug
```

Then restart Home Assistant and check logs:

1. **Settings** > **System** > **Logs**
2. Look for entries from `custom_components.tcp_to_event_converter`
3. Should see:
   - "TCP Server started on port X"
   - "Connection established from (IP, PORT)"
   - "Received raw payload: device:button:action"
   - "Firing event tcp_event with data: {...}"

### Log Levels

- **DEBUG**: Connection details, raw payloads, task cancellations
- **INFO**: Server start/stop, connections, event firing
- **WARNING**: Invalid messages, non-UTF-8 data, shutdown timeouts
- **ERROR**: Server startup failures, unexpected exceptions

## Quick Test Script

Here's a complete test script you can run:

```python
#!/usr/bin/env python3
"""
TCP to Event Converter Test Suite
Run this script to test your integration
"""

import socket
import time

# Configuration
HOST = "192.168.1.100"  # Change to your Home Assistant IP
PORT = 54321            # Change to your configured port

def test_connection(host, port):
    """Test if server is reachable."""
    print(f"\n[TEST] Connection Test to {host}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        sock.close()
        print("✓ Connection successful")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def send_message(host, port, message):
    """Send a message to the TCP server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            sock.connect((host, port))
            sock.sendall(message.encode('utf-8'))
            print(f"  Sent: {message.strip()}")
            return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def run_tests(host, port):
    """Run all test cases."""
    if not test_connection(host, port):
        print("\n❌ Cannot connect to server. Is it running?")
        return

    tests = [
        ("Valid message #1", "living_room:button_1:press"),
        ("Valid message #2", "bedroom:switch_2:toggle"),
        ("Valid message #3", "kitchen:sensor_3:motion"),
        ("Invalid format (too few)", "invalid:format"),
        ("Invalid format (too many)", "too:many:parts:here:now"),
    ]

    print(f"\n[TEST] Sending test messages")
    for name, message in tests:
        print(f"\n{name}:")
        send_message(host, port, message + "\n")
        time.sleep(0.5)

    print("\n✓ Test suite complete!")
    print("Check Home Assistant Developer Tools > Events for 'tcp_event'")

if __name__ == "__main__":
    print("=" * 60)
    print("TCP to Event Converter - Test Suite")
    print("=" * 60)
    run_tests(HOST, PORT)
```

## Action Items

When you run this test command, you should:

1. **Ask the user** for their Home Assistant IP and configured port
2. **Provide** the appropriate test method based on their environment
3. **Generate** a custom test script if needed
4. **Verify** the integration is running and accessible
5. **Monitor** Home Assistant logs for issues
6. **Check** that events are being fired correctly
7. **Suggest** debugging steps if tests fail

## Common Issues During Testing

### Connection Refused
- Server not running (check integration is loaded)
- Wrong port number
- Firewall blocking connection

### No Events Firing
- Wrong event type in Developer Tools
- Message format incorrect
- Check debug logs for errors

### Timeout Issues
- Network connectivity problem
- Server overwhelmed (unlikely)
- Firewall with stateful inspection

## Next Steps

After basic testing works:

1. Create an automation using the events
2. Test from actual target device (ESP32, Arduino, etc.)
3. Test under load (multiple rapid messages)
4. Test integration reload behavior
5. Test with firewall rules applied
