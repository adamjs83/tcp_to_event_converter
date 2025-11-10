---
name: Bug report
about: Create a report to help improve the integration
title: '[BUG] '
labels: bug, alpha
assignees: ''
---

**ALPHA SOFTWARE NOTICE**
This integration is in ALPHA stage. Some bugs and issues are expected. Thank you for helping test and improve it!

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Configure integration with '...'
2. Send TCP message '....'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened.

**Environment (please complete the following information):**
- Integration Version: [e.g., 0.1.0-alpha.1]
- Home Assistant Version: [e.g., 2024.11.0]
- Installation Method: [HACS / Manual]
- Home Assistant Installation Type: [e.g., Home Assistant OS, Container, Core, Supervised]

**Configuration:**
```yaml
# Your integration configuration (remove sensitive data)
TCP Port: 54321
Event Type: tcp_event
```

**Logs**
Please enable debug logging and paste relevant log entries:

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.tcp_to_event_converter: debug
```

```
Paste logs here
```

**Additional context**
Add any other context about the problem here.

**Testing performed**
- [ ] Tested with netcat/telnet
- [ ] Checked Home Assistant logs
- [ ] Verified configuration
- [ ] Restarted Home Assistant
- [ ] Checked firewall settings
