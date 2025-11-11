# Release Guide for TCP to Event Converter

This guide explains how to create new releases for this alpha-stage integration.

## Current Version Format

```
0.MINOR.PATCH-alpha.BUILD
```

**Current:** `0.1.0-alpha.1`

## Alpha Release Checklist

### 1. Determine Version Number

**For bug fixes and minor changes:**
- Increment BUILD: `0.1.0-alpha.1` → `0.1.0-alpha.2`

**For new features or significant changes:**
- Increment MINOR: `0.1.0-alpha.1` → `0.2.0-alpha.1`
- Reset BUILD to 1

**For major refactors or breaking changes:**
- Increment PATCH or MINOR based on scope
- Document breaking changes clearly

### 2. Update Version Numbers

Update the version in these files:

**1. manifest.json** (REQUIRED)
```json
{
  "version": "0.X.X-alpha.X"
}
```
Location: `custom_components/tcp_to_event_converter/manifest.json`

**2. README.md** (REQUIRED)
Update the version badge:
```markdown
[![Version](https://img.shields.io/badge/version-0.X.X--alpha.X-orange.svg)]
```
Location: Line 3 of `README.md`

### 3. Update CHANGELOG

Add a new section at the top of the Changelog in README.md:

```markdown
### Version 0.X.X-alpha.X (YYYY-MM-DD)
**ALPHA RELEASE - EXPERIMENTAL**

- Change 1
- Change 2
- Bug fix 1
```

### 4. Commit Changes

```bash
git add custom_components/tcp_to_event_converter/manifest.json
git add README.md
git commit -m "Bump version to 0.X.X-alpha.X"
```

### 5. Create Git Tag

```bash
# Create annotated tag
git tag -a v0.X.X-alpha.X -m "Release version 0.X.X-alpha.X"

# Push commits and tags
git push origin main
git push origin v0.X.X-alpha.X
```

### 6. Create GitHub Release

1. Go to https://github.com/adamjs83/tcp_to_event_converter/releases
2. Click "Draft a new release"
3. Select the tag you just created (`v0.X.X-alpha.X`)
4. Set release title: `v0.X.X-alpha.X - ALPHA`
5. Add release notes (copy from CHANGELOG)
6. Check "This is a pre-release" (IMPORTANT for alpha!)
7. Click "Publish release"

### 7. GitHub Release Template

```markdown
# TCP to Event Converter v0.X.X-alpha.X

> ⚠️ **ALPHA RELEASE - EXPERIMENTAL SOFTWARE**
>
> This is an alpha release. Expect bugs, breaking changes, and incomplete features.
> NOT recommended for production use. Use at your own risk.

## What's Changed

- Feature/fix 1
- Feature/fix 2
- Bug fix 1

## Installation

### HACS (Recommended)
1. Add custom repository: `https://github.com/adamjs83/tcp_to_event_converter`
2. Search for "TCP to Event Converter"
3. Install version `0.X.X-alpha.X`
4. Restart Home Assistant

### Manual Installation
Download the `Source code` zip below and extract to:
`<config_dir>/custom_components/tcp_to_event_converter/`

## Known Issues

- List any known issues
- Or link to GitHub Issues

## Testing

Please test and report issues at:
https://github.com/adamjs83/tcp_to_event_converter/issues

## Full Changelog

See [README.md](README.md#changelog) for complete changelog.
```

## Quick Command Reference

```bash
# Check current version
cat custom_components/tcp_to_event_converter/manifest.json | grep version

# Update to new alpha build (e.g., alpha.1 → alpha.2)
NEW_VERSION="0.1.0-alpha.2"

# Update manifest.json
# (Use your editor to change the version)

# Update README.md badge
# (Use your editor to change the badge version)

# Commit and tag
git add custom_components/tcp_to_event_converter/manifest.json README.md
git commit -m "Bump version to ${NEW_VERSION}"
git tag -a "v${NEW_VERSION}" -m "Release version ${NEW_VERSION}"
git push origin main
git push origin "v${NEW_VERSION}"
```

## Version Progression Examples

### Bug Fix Release
```
0.1.0-alpha.1 → 0.1.0-alpha.2
```
**When:** Small bug fixes, documentation updates

### Feature Release
```
0.1.0-alpha.2 → 0.2.0-alpha.1
```
**When:** New features, significant improvements

### Transition to Beta
```
0.5.0-alpha.3 → 0.5.0-beta.1
```
**When:** Feature complete, ready for broader testing

### Stable Release
```
0.9.0-beta.5 → 1.0.0
```
**When:** Production ready, thoroughly tested

## Beta Release Changes

When transitioning to beta:

1. Change version format to `0.X.X-beta.X`
2. Update README badges from "alpha-red" to "beta-yellow"
3. Update warning messages to reflect beta status
4. Still mark as pre-release in GitHub
5. Update VERSION.md to reflect beta status

## Stable Release (1.0.0) Changes

When ready for stable:

1. Change version to `1.0.0`
2. Remove alpha/beta warnings from README
3. Update badges to show "stable-green"
4. Do NOT check "pre-release" in GitHub
5. Create comprehensive release notes
6. Announce on Home Assistant forums

## HACS Considerations

**IMPORTANT:** HACS requires GitHub Releases, not just Git tags!

- HACS detects new releases from **GitHub Releases** (not Git tags alone)
- A GitHub Release must be created for each version for HACS to show the version number
- Without a GitHub Release, HACS will show a commit ID instead of the version
- Pre-release flag ensures users know it's alpha (required for alpha/beta)
- Version number displays in HACS interface only after GitHub Release is created
- HACS may take 5-10 minutes to detect new releases

### Automated Release Creation

This repository includes a GitHub Actions workflow that automatically creates releases when you push tags:

1. Push a tag: `git push origin v0.X.X-alpha.X`
2. GitHub Actions automatically creates the release
3. HACS detects the release within 5-10 minutes

The workflow (`.github/workflows/release.yml`) handles:
- Version validation against manifest.json
- Release notes generation from tag message
- Pre-release marking for alpha/beta versions
- Automatic release publication

## Common Mistakes to Avoid

- ❌ **Creating only a Git tag without a GitHub Release** (HACS won't show version)
- ❌ Forgetting to mark as "pre-release" in GitHub
- ❌ Not updating README badge version
- ❌ Skipping CHANGELOG updates
- ❌ Creating tag without 'v' prefix
- ❌ Not testing before release
- ❌ Forgetting to push tags
- ❌ Tag version not matching manifest.json version

## Hotfix Process

For critical bugs in alpha:

1. Create fix immediately
2. Increment build number
3. Follow normal release process
4. Add "HOTFIX" to release title
5. Clearly document what was fixed

Example:
```
v0.1.0-alpha.2 - ALPHA HOTFIX
```

## Questions?

See [VERSION.md](VERSION.md) for versioning strategy details.
