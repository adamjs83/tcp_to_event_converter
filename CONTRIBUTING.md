# Contributing to TCP to Event Converter

Thank you for your interest in contributing to this project! As an **ALPHA** stage project, we especially appreciate early adopters helping to test, report issues, and improve the integration.

## Project Status: ALPHA

This integration is in early **ALPHA** development. This means:

- The codebase is evolving rapidly
- Breaking changes may occur between releases
- Documentation may be incomplete
- Some features may be experimental

Your contributions are valuable in moving this project toward stability!

## How to Contribute

### Reporting Bugs

Bug reports are crucial for an alpha project. Please:

1. Check existing [issues](https://github.com/adamjs83/tcp_to_event_converter/issues) first
2. Use the bug report template
3. Include:
   - Integration version (from manifest.json)
   - Home Assistant version
   - Detailed steps to reproduce
   - Relevant logs with debug logging enabled
   - Your configuration (sanitized)

### Suggesting Features

Feature requests are welcome! Please:

1. Check existing issues to avoid duplicates
2. Use the feature request template
3. Explain the use case clearly
4. Consider whether it fits the project scope

### Testing

Testing is especially valuable during alpha:

- Test with different devices and message formats
- Test edge cases and error conditions
- Test on different Home Assistant setups
- Report what works AND what doesn't work

### Code Contributions

#### Before You Start

1. Open an issue to discuss major changes
2. Check if someone else is already working on it
3. Fork the repository
4. Create a feature branch

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/tcp_to_event_converter.git
cd tcp_to_event_converter

# Create a branch
git checkout -b feature/your-feature-name
```

#### Code Standards

Please follow these guidelines:

**Python Style:**
- Follow PEP 8
- Use type hints
- Add docstrings for functions and classes
- Keep functions focused and small

**Home Assistant Integration:**
- Follow [Home Assistant integration quality scale](https://developers.home-assistant.io/docs/integration_quality_scale_index/)
- Use async/await properly (no blocking I/O)
- Add proper logging
- Handle errors gracefully
- Use Home Assistant helpers where appropriate

**Example Code Style:**

```python
async def handle_connection(
    self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """Handle an incoming TCP connection.

    Args:
        reader: The stream reader for incoming data
        writer: The stream writer for responses
    """
    addr = writer.get_extra_info("peername")
    _LOGGER.debug("Connection established from %s", addr)

    try:
        # Your code here
        pass
    except Exception as err:
        _LOGGER.error("Error handling connection from %s: %s", addr, err)
    finally:
        await self._cleanup_connection(writer)
```

#### Testing Your Changes

1. Test in a real Home Assistant environment
2. Enable debug logging
3. Test error conditions
4. Test shutdown/reload behavior
5. Verify no blocking operations

#### Commit Guidelines

Write clear commit messages:

```bash
# Good commit messages
git commit -m "Fix: Handle connection timeout gracefully"
git commit -m "Add: Support for custom message delimiters"
git commit -m "Docs: Update installation instructions"

# Use prefixes
# Fix: Bug fixes
# Add: New features
# Update: Improvements to existing features
# Docs: Documentation changes
# Refactor: Code refactoring
# Test: Test additions or changes
```

#### Pull Request Process

1. Update documentation if needed
2. Update CHANGELOG.md with your changes
3. Ensure your code follows the style guidelines
4. Test thoroughly in Home Assistant
5. Create a pull request with:
   - Clear description of changes
   - Reference to related issues
   - Testing performed
   - Screenshots if applicable

**Pull Request Template:**

```markdown
## Description
Brief description of what this PR does

## Related Issues
Fixes #123

## Changes Made
- Change 1
- Change 2

## Testing Performed
- [ ] Tested in Home Assistant 2024.11.0
- [ ] Tested with various message formats
- [ ] Tested error handling
- [ ] Checked logs for errors

## Breaking Changes
None / Describe any breaking changes

## Additional Notes
Any other relevant information
```

### Documentation Contributions

Documentation improvements are always welcome:

- Fix typos or unclear instructions
- Add examples
- Improve troubleshooting guides
- Add use cases

## Code Review Process

For this alpha project:

1. Maintainers will review PRs as time permits
2. Expect feedback and discussion
3. Be patient - this is a volunteer effort
4. Be open to suggested changes

## Communication

- **Issues:** For bugs, features, and questions
- **Discussions:** For general questions and ideas
- **Pull Requests:** For code contributions

## Alpha Development Priorities

During the alpha phase, we prioritize:

1. **Stability:** Fixing crashes and critical bugs
2. **Core Functionality:** Ensuring basic features work reliably
3. **Security:** Addressing security concerns
4. **Documentation:** Clear setup and usage instructions
5. **New Features:** After core stability is achieved

## What We're Looking For

Especially valuable during alpha:

- Bug reports with detailed reproduction steps
- Testing on various Home Assistant setups
- Performance testing
- Security reviews
- Edge case testing
- Documentation improvements
- Code quality improvements

## What to Avoid

Please don't:

- Submit large, unannounced refactors
- Add features without discussion
- Ignore existing code style
- Submit untested code
- Include unrelated changes in PRs

## Recognition

Contributors will be:

- Listed in release notes
- Credited in the repository
- Appreciated in the community!

## Questions?

If you're unsure about anything:

1. Open an issue with your question
2. Check existing documentation
3. Look at existing code for examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Thank You!

Every contribution, no matter how small, helps make this integration better. Thank you for being an early supporter of this alpha project!

---

**Remember:** This is an ALPHA project. We're all learning and improving together. Don't be afraid to ask questions or make mistakes. We appreciate your help!
