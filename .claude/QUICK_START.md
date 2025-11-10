# Quick Start Guide - Automated Releases

## TL;DR

To release a new version:
```
/release
```

That's it! The automation handles everything.

## What It Does

1. Bumps version: `0.1.0-alpha.1` → `0.1.0-alpha.2`
2. Updates `manifest.json`
3. Commits changes
4. Creates git tag
5. Pushes to Gitea

## Common Commands

```bash
# Standard release (auto-increment)
/release

# Custom version
/release 0.1.0-alpha.5

# Commit locally but don't push
/release --skip-push

# Check current version
python3 .claude/scripts/version_bump.py --show
```

## Troubleshooting

**Problem**: "Uncommitted changes"
**Solution**: Commit or stash your changes first

**Problem**: "Not on main branch"
**Solution**: Switch to main: `git checkout main`

**Problem**: "Push failed"
**Solution**: Check your network and Gitea credentials

## Files That Matter

- **manifest.json**: Version is stored here
  ```
  custom_components/tcp_to_event_converter/manifest.json
  ```

- **Release command**: Controls the automation
  ```
  .claude/commands/release.md
  ```

- **Version script**: Handles version bumping
  ```
  .claude/scripts/version_bump.py
  ```

## Full Documentation

See `AUTOMATION.md` for complete details.

## Remote Repository

- **Gitea**: https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer.git
- **Branch**: main
- **Tags**: Created automatically with format `v0.1.0-alpha.X`
