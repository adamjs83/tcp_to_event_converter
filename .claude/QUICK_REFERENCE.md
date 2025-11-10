# Quick Reference - Automated Version Management

## Fastest Way to Commit Changes (Automatic)

```bash
# Make your changes, then:
git add -A
git commit -m "Your descriptive message"

# That's it! Automatic:
# ✓ Version incremented (0.1.0-alpha.1 → 0.1.0-alpha.2)
# ✓ manifest.json updated
# ✓ Git tag created (v0.1.0-alpha.2)
# ✓ Pushed to Gitea
```

## Common Commands

### Daily Development (Automated with Hooks)

```bash
# Regular commit (auto-versions and pushes)
git add -A
git commit -m "Add feature X"

# Work-in-progress (bypass auto-push)
git commit --no-verify -m "WIP: Testing"
```

### Claude Code Commands

```bash
# Quick commit with auto-version
/commit

# Formal release with options
/release                    # Auto-increment
/release 0.1.0-alpha.15    # Set specific version
/release --skip-push       # Local only
```

### Manual Version Control

```bash
# Show current version
python3 .claude/scripts/version_bump.py --show

# Increment version manually
python3 .claude/scripts/version_bump.py

# Set specific version
python3 .claude/scripts/version_bump.py 0.1.0-alpha.10
```

## Troubleshooting

### Hooks Not Running

```bash
# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit

# Test hooks
bash .claude/scripts/test_hooks.sh
```

### Disable Auto-Push

```bash
# Edit post-commit hook
vim .git/hooks/post-commit

# Change this line:
AUTO_PUSH_ENABLED=false
```

### Fix Version Issues

```bash
# Check current version
python3 .claude/scripts/version_bump.py --show

# Manually set correct version
python3 .claude/scripts/version_bump.py 0.1.0-alpha.5
```

## File Locations

- **Manifest**: `custom_components/tcp_to_event_converter/manifest.json`
- **Version Script**: `.claude/scripts/version_bump.py`
- **Pre-commit Hook**: `.git/hooks/pre-commit`
- **Post-commit Hook**: `.git/hooks/post-commit`
- **Full Guide**: `.claude/GIT_HOOKS_GUIDE.md`

## Git Remote

- **URL**: https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer.git
- **Remote**: origin
- **Branch**: main

## Version Format

Pattern: `MAJOR.MINOR.PATCH-alpha.BUILD`

Example progression:
```
0.1.0-alpha.1   (current)
0.1.0-alpha.2   (after next commit)
0.1.0-alpha.3   (after next commit)
...
```

## Documentation

- **Quick Reference**: `.claude/QUICK_REFERENCE.md` (this file)
- **Git Hooks Guide**: `.claude/GIT_HOOKS_GUIDE.md` (comprehensive)
- **Automation Overview**: `.claude/AUTOMATION.md` (all options)
- **Release Command**: `.claude/commands/release.md`
- **Commit Command**: `.claude/commands/commit.md`

## Test Everything

```bash
# Run full test suite
bash .claude/scripts/test_hooks.sh
```

## Remember

- ✅ Every commit auto-increments version
- ✅ Every commit creates a git tag
- ✅ Every commit pushes to Gitea (on main branch)
- ⚠️ Use `--no-verify` for WIP commits
- ⚠️ Hooks only work on `main` branch by default
