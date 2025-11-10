# HACS Troubleshooting Guide

This guide helps resolve common issues with HACS integration.

## Issue: HACS Shows Commit ID Instead of Version Number

### Symptom
When you click "Download" in HACS, it shows a commit hash (e.g., `fafbbd0`) instead of the version number (e.g., `v0.1.0-alpha.1`).

### Root Cause
**HACS requires GitHub Releases, not just Git tags.**

A Git tag alone is insufficient. HACS uses the GitHub API to fetch releases, and without a GitHub Release, it falls back to showing the commit ID.

### Solution

#### Step 1: Verify Git Tag Exists
```bash
# Check local tags
git tag -l

# Check remote tags
git ls-remote --tags origin
```

You should see your tag (e.g., `v0.1.0-alpha.1`) in both outputs.

#### Step 2: Create GitHub Release

**Option A: Via GitHub Web Interface (Recommended)**

1. Go to: https://github.com/adamjs83/tcp_to_event_converter/releases
2. Click "Draft a new release"
3. Choose existing tag: `v0.1.0-alpha.1`
4. Fill in release details:
   - **Title**: `TCP to Event Converter v0.1.0-alpha.1`
   - **Description**: Add release notes (see template below)
   - **Pre-release**: ✓ Check this box (for alpha/beta versions)
5. Click "Publish release"

**Option B: Via GitHub CLI**

```bash
gh release create v0.1.0-alpha.1 \
  --title "TCP to Event Converter v0.1.0-alpha.1" \
  --notes "Release notes here..." \
  --prerelease
```

**Option C: Via Included Script**

```bash
# Set your GitHub token
export GITHUB_TOKEN="your_github_token_here"

# Run the script
./create_github_release.sh
```

#### Step 3: Verify Release Created

Visit: https://github.com/adamjs83/tcp_to_event_converter/releases

You should see your release with a "Pre-release" badge.

#### Step 4: Wait for HACS to Update

- HACS caches release information
- Wait 5-10 minutes for HACS to detect the new release
- You can force refresh by reloading HACS in Home Assistant

#### Step 5: Verify in HACS

1. Open Home Assistant
2. Go to HACS > Integrations
3. Search for "TCP to Event Converter"
4. You should now see `v0.1.0-alpha.1` instead of a commit ID

---

## Issue: HACS Doesn't Show Integration at All

### Possible Causes

1. **Repository not added to HACS**
2. **Invalid hacs.json configuration**
3. **Missing manifest.json**

### Solution

#### 1. Add as Custom Repository

In HACS:
1. Click three dots menu → Custom repositories
2. Add repository URL: `https://github.com/adamjs83/tcp_to_event_converter`
3. Category: `Integration`
4. Click "Add"

#### 2. Verify hacs.json

Location: `/hacs.json` (repository root)

Required content:
```json
{
  "name": "TCP to Event Converter",
  "render_readme": true,
  "homeassistant": "2023.1.0",
  "content_in_root": false,
  "zip_release": false,
  "filename": "tcp_to_event_converter"
}
```

Key settings:
- `content_in_root: false` - Integration is in `custom_components/` subdirectory
- `filename` - Must match the integration domain in manifest.json

#### 3. Verify manifest.json

Location: `/custom_components/tcp_to_event_converter/manifest.json`

Required fields:
```json
{
  "domain": "tcp_to_event_converter",
  "name": "TCP to Event Converter",
  "version": "0.1.0-alpha.1",
  "documentation": "https://github.com/adamjs83/tcp_to_event_converter",
  "config_flow": true
}
```

---

## Issue: HACS Shows Wrong Version

### Symptom
HACS shows an old version number or incorrect version.

### Solution

1. **Check manifest.json version matches tag**:
   ```bash
   cat custom_components/tcp_to_event_converter/manifest.json | grep version
   git tag -l
   ```

2. **Ensure GitHub Release exists for the version**:
   - Visit: https://github.com/adamjs83/tcp_to_event_converter/releases
   - Verify release exists for the tag

3. **Force HACS cache refresh**:
   - In HACS, click three dots → Reload HACS
   - Wait 1-2 minutes
   - Check again

4. **Check GitHub Release is not draft**:
   - Draft releases are not visible to HACS
   - Must be published (can be pre-release)

---

## Issue: Users Can't See Alpha Versions

### Symptom
Users report they can't find your alpha version in HACS.

### Cause
HACS hides pre-releases by default to protect users from installing unstable software.

### Solution

Users must enable experimental features in HACS:

1. Go to HACS settings
2. Enable "Enable AppDaemon apps discovery & tracking"
3. Enable "Show beta versions" (or similar option)
4. Reload HACS
5. Search for your integration

**Note**: This is intentional HACS behavior. Alpha/beta versions should not be easily accessible to prevent accidental installation by inexperienced users.

---

## Issue: GitHub Actions Workflow Not Creating Release

### Symptom
You pushed a tag but GitHub Actions didn't create a release.

### Solution

1. **Check workflow file exists**:
   ```bash
   ls -la .github/workflows/release.yml
   ```

2. **Verify workflow syntax**:
   - Go to: https://github.com/adamjs83/tcp_to_event_converter/actions
   - Check for failed workflow runs
   - Click on failed run to see error details

3. **Check GitHub Actions permissions**:
   - Go to: Settings → Actions → General
   - Ensure "Workflow permissions" is set to "Read and write permissions"
   - Save changes

4. **Verify tag format**:
   - Workflow triggers on tags starting with `v`
   - Example: `v0.1.0-alpha.1` ✓
   - Example: `0.1.0-alpha.1` ✗

5. **Re-run workflow manually**:
   - Go to Actions tab
   - Select the failed workflow
   - Click "Re-run all jobs"

---

## Release Notes Template

Use this template when creating GitHub Releases manually:

```markdown
# TCP to Event Converter v0.1.0-alpha.1

**Status: ALPHA - Experimental software, not production ready**

Breaking changes may occur in future releases.

## Features
- TCP server listening on configurable port
- Converts TCP messages to Home Assistant events
- UI-based configuration through config flow
- Comprehensive error handling and validation
- HACS compatible structure

## Installation

### Via HACS (Recommended)
1. Add custom repository: `https://github.com/adamjs83/tcp_to_event_converter`
2. Search for "TCP to Event Converter"
3. Enable "Show beta versions" in HACS experimental settings
4. Click Download
5. Restart Home Assistant

### Manual Installation
1. Download Source Code (zip) below
2. Extract archive
3. Copy `custom_components/tcp_to_event_converter` to your Home Assistant config
4. Restart Home Assistant

## Known Limitations

This is an alpha release. Please report issues on GitHub.

## Documentation

- [README](https://github.com/adamjs83/tcp_to_event_converter/blob/main/README.md)
- [Configuration Guide](https://github.com/adamjs83/tcp_to_event_converter/blob/main/README.md#configuration)
- [Version History](https://github.com/adamjs83/tcp_to_event_converter/blob/main/VERSION.md)

## Support

Report issues at: https://github.com/adamjs83/tcp_to_event_converter/issues
```

---

## Automated Release Workflow

This repository includes `.github/workflows/release.yml` that automatically:

1. **Triggers** when you push a tag starting with `v`
2. **Validates** tag version matches manifest.json
3. **Extracts** tag message for release notes
4. **Creates** GitHub Release with proper pre-release flag
5. **Publishes** release (HACS detects within 5-10 minutes)

### Using the Automated Workflow

```bash
# 1. Update manifest.json version
# 2. Commit changes
git add custom_components/tcp_to_event_converter/manifest.json
git commit -m "Bump version to 0.1.0-alpha.2"

# 3. Create annotated tag with detailed message
git tag -a v0.1.0-alpha.2 -m "Release version 0.1.0-alpha.2

Features:
- Feature 1
- Feature 2

Bug Fixes:
- Fix 1
- Fix 2"

# 4. Push commit and tag
git push origin main
git push origin v0.1.0-alpha.2

# 5. GitHub Actions automatically creates the release
# 6. Check Actions tab for workflow progress
# 7. HACS detects new release within 5-10 minutes
```

---

## Verification Checklist

Before reporting issues, verify:

- [ ] Git tag exists and is pushed to GitHub
- [ ] GitHub Release exists (not just tag)
- [ ] Release is marked as "Pre-release" (for alpha/beta)
- [ ] Release is published (not draft)
- [ ] Tag version matches manifest.json version
- [ ] hacs.json exists and is valid
- [ ] manifest.json exists in correct location
- [ ] Waited at least 10 minutes after creating release
- [ ] Reloaded HACS in Home Assistant

---

## Getting Help

If you've followed all troubleshooting steps and still have issues:

1. **Check HACS logs**:
   - Home Assistant → Settings → System → Logs
   - Filter for "HACS"

2. **Verify repository structure**:
   ```
   tcp_to_event_converter/
   ├── hacs.json                          ← Must exist
   ├── custom_components/
   │   └── tcp_to_event_converter/
   │       ├── manifest.json              ← Must exist
   │       ├── __init__.py
   │       └── ...
   └── .github/
       └── workflows/
           └── release.yml                ← Optional but recommended
   ```

3. **Report issue**:
   - Create issue at: https://github.com/adamjs83/tcp_to_event_converter/issues
   - Include:
     - HACS version
     - Home Assistant version
     - Screenshot of HACS interface showing the problem
     - Link to your GitHub Release
     - Any relevant error logs

---

## Additional Resources

- [HACS Documentation](https://hacs.xyz/)
- [HACS Repository Requirements](https://hacs.xyz/docs/publish/start)
- [Home Assistant Integration Requirements](https://developers.home-assistant.io/docs/creating_integration_manifest)
- [Semantic Versioning Guide](https://semver.org/)
