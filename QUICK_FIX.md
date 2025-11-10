# Quick Fix: HACS Shows Commit ID Instead of Version

## The Problem
HACS displays a commit hash (e.g., `fafbbd0`) instead of your version number (e.g., `v0.1.0-alpha.1`).

## The Cause
**You created a Git tag but not a GitHub Release.**

HACS requires GitHub Releases to display version numbers. Git tags alone are not enough.

## The Fix (Choose One Method)

### Method 1: Web Interface (Easiest - 2 minutes)

1. **Go to releases page**: https://github.com/adamjs83/tcp_to_event_converter/releases

2. **Click**: "Draft a new release"

3. **Fill form**:
   - **Choose a tag**: Select `v0.1.0-alpha.1` from dropdown
   - **Release title**: `TCP to Event Converter v0.1.0-alpha.1`
   - **Description**: Copy/paste:
     ```
     First alpha release of TCP to Event Converter integration.

     **Status: ALPHA - Experimental software**

     Features:
     - TCP server listening on configurable port
     - Converts TCP messages to Home Assistant events
     - UI-based configuration through config flow
     - Comprehensive error handling and validation
     - HACS compatible structure

     Install via HACS by adding this repository as a custom repository.
     ```
   - **Pre-release**: ✓ CHECK THIS BOX (required for alpha)

4. **Click**: "Publish release"

5. **Wait**: 5-10 minutes for HACS to detect the release

6. **Verify**: Check HACS again - should show `v0.1.0-alpha.1`

### Method 2: GitHub CLI (If Installed)

```bash
cd "/Users/adamjs83/Library/Mobile Documents/com~apple~CloudDocs/aiworkflows/tcp_to_event_converer"

gh release create v0.1.0-alpha.1 \
  --title "TCP to Event Converter v0.1.0-alpha.1" \
  --notes "First alpha release. Status: ALPHA - Experimental software" \
  --prerelease
```

### Method 3: Using Provided Script

```bash
cd "/Users/adamjs83/Library/Mobile Documents/com~apple~CloudDocs/aiworkflows/tcp_to_event_converer"

# Set your GitHub token (get from https://github.com/settings/tokens)
export GITHUB_TOKEN="your_token_here"

# Run script
./create_github_release.sh
```

## Future Releases

For all future releases, the GitHub Actions workflow will automatically create releases when you push tags:

```bash
# Just push the tag - GitHub Actions does the rest!
git tag -a v0.2.0-alpha.1 -m "Release notes here"
git push origin v0.2.0-alpha.1
```

GitHub Actions automatically creates the release within seconds.

## Verification

After creating the release:

1. ✓ Visit: https://github.com/adamjs83/tcp_to_event_converter/releases
2. ✓ Confirm release exists with "Pre-release" badge
3. ✓ Wait 5-10 minutes
4. ✓ Reload HACS in Home Assistant
5. ✓ Check integration - should show `v0.1.0-alpha.1`

## Still Not Working?

See [HACS_TROUBLESHOOTING.md](HACS_TROUBLESHOOTING.md) for detailed troubleshooting.

## Remember

**Git Tag ≠ GitHub Release**

- **Git Tag**: Repository marker (invisible to HACS)
- **GitHub Release**: Published release (visible to HACS) ✓

Always create both for HACS to work properly!
