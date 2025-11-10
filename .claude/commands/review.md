# Review Changes

You are helping review code changes in the TCP to Event Converter Home Assistant integration before committing them.

## Your Task

Perform a thorough review of uncommitted changes to ensure quality, correctness, and compliance with Home Assistant integration standards.

## Review Process

### 1. Show Current Changes

First, display what has changed:

```bash
# Show status
git status

# Show all changes (staged and unstaged)
git diff HEAD

# Show only staged changes
git diff --cached

# Show file names only
git diff --name-only HEAD
```

### 2. Review Each Changed File

For each modified file, analyze:

**Code Changes:**
- What was changed and why?
- Does the change make sense?
- Are there any unintended side effects?
- Is the change complete or are related changes needed?

**Quality Checks:**
- Type hints present and correct?
- Error handling adequate?
- Logging appropriate?
- Comments/docstrings updated?
- No debug code left behind?

**Home Assistant Standards:**
- Follows async/await patterns?
- Proper resource cleanup?
- Compatible with HA integration guidelines?
- Config flow changes need translation updates?

### 3. Check for Common Issues

**Before Committing:**
- [ ] No debug print statements
- [ ] No commented-out code (unless intentional)
- [ ] No TODOs or FIXMEs without issues filed
- [ ] No hardcoded values that should be configurable
- [ ] No sensitive information (passwords, tokens, IPs)
- [ ] Version numbers updated (manifest.json, README.md)
- [ ] Changelog updated for user-facing changes
- [ ] README updated if behavior changed
- [ ] Type hints added/updated
- [ ] Docstrings added/updated
- [ ] Error messages are helpful
- [ ] Log levels appropriate

### 4. Test Considerations

**Has this been tested?**
- Manual testing completed?
- Edge cases considered?
- Error cases tested?
- Integration reload tested?
- No regressions introduced?

### 5. Breaking Changes

**Check for breaking changes:**
- Configuration format changed?
- Event data structure changed?
- Default values changed?
- API/interface changes?

If yes, these need:
- Clear documentation in changelog
- Migration guide if needed
- Version bump (major/minor)

## Review Checklist

### Code Quality
- [ ] Code is readable and maintainable
- [ ] Functions are focused and not too complex
- [ ] Variable names are clear and descriptive
- [ ] No unnecessary code duplication
- [ ] Follows existing code style

### Home Assistant Integration
- [ ] Async/await used correctly
- [ ] No blocking calls in async functions
- [ ] Resources properly cleaned up
- [ ] Error handling returns appropriate values
- [ ] Logging uses _LOGGER consistently
- [ ] Config entry handling correct

### Security
- [ ] Input validation adequate
- [ ] No new security vulnerabilities
- [ ] Error messages don't leak sensitive info
- [ ] Network operations safe
- [ ] No SQL injection, XSS, or similar issues

### Documentation
- [ ] README reflects changes
- [ ] Inline comments explain complex logic
- [ ] Changelog updated
- [ ] Version bumped if needed

### Testing
- [ ] Changes are testable
- [ ] Edge cases considered
- [ ] Error paths tested
- [ ] Manual testing completed

## Review Output Format

Provide feedback in this format:

### Summary
[Brief overview of changes]

### Files Changed
- `file1.py`: [Description of changes]
- `file2.py`: [Description of changes]

### Positive Findings
- [Things done well]

### Issues Found

**[SEVERITY] Issue Title**
- **File**: `filename.py` (line X)
- **Issue**: [Description]
- **Recommendation**: [How to fix]

### Recommendations
1. [Specific actionable recommendations]

### Approval Status
- [ ] Approved - Ready to commit
- [ ] Approved with minor comments
- [ ] Changes requested - Must fix before commit
- [ ] Rejected - Major issues found

## Specific Review Points

### For tcp_server.py Changes

Check:
- Task management correct?
- Connection cleanup proper?
- Timeout handling safe?
- Error handling comprehensive?
- No race conditions?
- Memory leaks possible?

### For __init__.py Changes

Check:
- Setup returns correct values?
- Teardown cleans up properly?
- Error handling complete?
- hass.data usage correct?

### For config_flow.py Changes

Check:
- Input validation thorough?
- User feedback clear?
- Error messages helpful?
- Translations needed?

### For manifest.json Changes

Check:
- Version incremented appropriately?
- Dependencies up to date?
- Required fields present?
- Version follows semantic versioning?

### For README.md Changes

Check:
- Examples still accurate?
- Installation steps current?
- Configuration docs complete?
- Changelog updated?

## Pre-Commit Actions

Before allowing a commit:

1. **Run linters** (if available):
   ```bash
   black --check .
   pylint custom_components/tcp_to_event_converter/
   ```

2. **Check for sensitive data**:
   ```bash
   git diff HEAD | grep -i "password\|token\|secret\|key"
   ```

3. **Verify version bump** (if needed):
   ```bash
   git diff HEAD manifest.json | grep version
   git diff HEAD README.md | grep "Version"
   ```

4. **Check for debug code**:
   ```bash
   git diff HEAD | grep -i "print(\|console\.\|debugger"
   ```

## Commit Message Suggestions

Based on changes, suggest appropriate commit message:

**Format:**
```
<type>: <short description>

<detailed description>

<breaking changes if any>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
fix: Prevent shutdown timeout with active TCP connections

- Added proper task tracking for client connections
- Implemented graceful cancellation with timeout
- Made stop() method idempotent to prevent double-stop

Fixes #123
```

```
feat: Add configurable connection timeout

- Added CONN_TIMEOUT config option
- Updated config flow with new field
- Added validation and defaults
- Updated documentation

Breaking change: Config entry format changed. Users must
reconfigure the integration.
```

## Action Items

When reviewing:

1. **Display all changes** using git diff
2. **Analyze each file** systematically
3. **Check for common issues** from checklist
4. **Verify testing** has been done
5. **Check documentation** is updated
6. **Assess security** implications
7. **Validate versioning** is correct
8. **Suggest improvements** where needed
9. **Provide clear feedback** with examples
10. **Give approval status** (ready/needs work/blocked)

## Questions to Ask User

- What prompted these changes?
- Have you tested the changes?
- Are there any known issues?
- Should the version be bumped?
- Are there related changes needed?
- Do automations need updating?

## Follow-up

After review, offer to:
- Create the commit with proper message
- Update documentation
- Create a changelog entry
- Run tests
- Create a pull request
