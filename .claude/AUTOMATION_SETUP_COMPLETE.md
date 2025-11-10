# Automation Setup Complete

## Summary

Your TCP to Event Converter project now has **fully automated version management and git operations**.

## What Was Configured

### 1. Git Hooks (NEW - Automatic)

**Pre-commit Hook** (`.git/hooks/pre-commit`):
- ✅ Automatically increments alpha version on every commit
- ✅ Updates `manifest.json` with new version
- ✅ Stages the updated manifest

**Post-commit Hook** (`.git/hooks/post-commit`):
- ✅ Creates annotated git tag for each version
- ✅ Automatically pushes commits to Gitea
- ✅ Automatically pushes tags to Gitea
- ✅ Configurable (can disable auto-push)

### 2. Claude Code Commands

**`/commit` Command** (`.claude/commands/commit.md`):
- Interactive commit with auto-versioning
- Smart commit message generation
- Preview before execution
- Supports flags: `--no-push`, `--dry-run`

**`/release` Command** (`.claude/commands/release.md` - existing):
- Manual release control
- Custom version specification
- Formal release workflow

### 3. Scripts and Tools

**Version Bump Script** (`.claude/scripts/version_bump.py`):
- Parses and validates version format
- Increments alpha build number
- Updates manifest.json safely
- Command-line tool for manual use

**Test Suite** (`.claude/scripts/test_hooks.sh`):
- Validates all automation components
- Tests version incrementation
- Checks git configuration
- Verifies hook installation

### 4. Documentation

**Comprehensive Guides**:
- ✅ `.claude/GIT_HOOKS_GUIDE.md` - Complete git hooks documentation
- ✅ `.claude/AUTOMATION.md` - Updated with all automation options
- ✅ `.claude/QUICK_REFERENCE.md` - Quick command reference
- ✅ `.claude/commands/commit.md` - /commit command docs
- ✅ `.claude/commands/release.md` - /release command docs (existing)

## How It Works

### Simple Workflow (Recommended)

```bash
# 1. Make your code changes
vim custom_components/tcp_to_event_converter/sensor.py

# 2. Commit (everything else is automatic)
git add -A
git commit -m "Add new sensor feature"

# Output you'll see:
# 🔄 Pre-commit hook: Auto-versioning...
# Current version: 0.1.0-alpha.1
# ✓ 0.1.0-alpha.1 → 0.1.0-alpha.2
# ✓ Staged updated manifest.json with version 0.1.0-alpha.2
# [main abc1234] Add new sensor feature
# 🚀 Post-commit hook: Processing release...
# Current version: 0.1.0-alpha.2
# ✓ Created tag: v0.1.0-alpha.2
# ✓ Pushed commit to origin/main
# ✓ Pushed tag to origin
# 🎉 Release 0.1.0-alpha.2 published to Gitea!
```

### What Happens Automatically

1. **Pre-commit**:
   - Version: `0.1.0-alpha.1` → `0.1.0-alpha.2`
   - File updated: `manifest.json` (line 4)
   - Staged: Updated manifest

2. **Commit**:
   - Your changes + updated manifest committed
   - Commit message: Your message

3. **Post-commit**:
   - Tag created: `v0.1.0-alpha.2`
   - Pushed to: `origin/main`
   - Tag pushed: `v0.1.0-alpha.2`

## Configuration Options

### Three Ways to Use Automation

| Method | When to Use | Command |
|--------|-------------|---------|
| **Git Hooks** | Daily development (automatic) | `git commit -m "message"` |
| **`/commit`** | Claude Code with preview | `/commit` |
| **`/release`** | Formal releases, custom versions | `/release` or `/release 0.1.0-alpha.15` |

### Customize Behavior

**Disable auto-push** (commit locally only):
```bash
vim .git/hooks/post-commit
# Change: AUTO_PUSH_ENABLED=false
```

**Disable auto-tagging**:
```bash
vim .git/hooks/post-commit
# Change: AUTO_TAG_ENABLED=false
```

**Bypass hooks temporarily**:
```bash
git commit --no-verify -m "WIP changes"
```

## Testing the Setup

### Run the Test Suite

```bash
cd "/Users/adamjs83/Library/Mobile Documents/com~apple~CloudDocs/aiworkflows/tcp_to_event_converer"
bash .claude/scripts/test_hooks.sh
```

### Test Results

All tests passed! ✅

- ✅ Hooks exist and are executable
- ✅ Version script works correctly
- ✅ manifest.json is valid
- ✅ Git is configured properly
- ✅ Remote URL is correct
- ✅ Current branch is main
- ✅ Version format is valid

## Quick Reference

### Show Current Version

```bash
python3 .claude/scripts/version_bump.py --show
```

### Manual Version Bump

```bash
# Auto-increment
python3 .claude/scripts/version_bump.py

# Set specific version
python3 .claude/scripts/version_bump.py 0.1.0-alpha.25
```

### Commit with Auto-versioning

```bash
git add -A
git commit -m "Your message"
```

### Commit Without Auto-versioning

```bash
git commit --no-verify -m "WIP"
```

### View Tags

```bash
git tag -l --sort=-version:refname
```

## File Structure

```
.claude/
├── commands/
│   ├── commit.md              # NEW - /commit command
│   └── release.md             # Existing - /release command
├── scripts/
│   ├── version_bump.py        # Existing - Version management
│   └── test_hooks.sh          # NEW - Test suite
├── AUTOMATION.md              # UPDATED - All automation options
├── GIT_HOOKS_GUIDE.md         # NEW - Comprehensive hooks guide
├── QUICK_REFERENCE.md         # NEW - Quick command reference
└── AUTOMATION_SETUP_COMPLETE.md  # NEW - This file

.git/hooks/
├── pre-commit                 # NEW - Auto-version on commit
└── post-commit                # NEW - Auto-tag and push

custom_components/tcp_to_event_converter/
└── manifest.json              # Auto-updated on every commit
```

## Project Configuration

- **Version**: 0.1.0-alpha.1 (current)
- **Version File**: `custom_components/tcp_to_event_converter/manifest.json`
- **Git Remote**: https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer.git
- **Branch**: main
- **Version Format**: `MAJOR.MINOR.PATCH-alpha.BUILD`

## Next Steps

1. **Test the automation**:
   ```bash
   # Create a trivial change to test
   echo "# Test automation" >> README.md
   git add README.md
   git commit -m "Test automated versioning"
   ```

2. **Verify on Gitea**:
   - Visit: https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer
   - Check commits tab for your commit
   - Check tags tab for new version tag

3. **Start developing**:
   - Make code changes as normal
   - Commit when ready
   - Everything else happens automatically!

## Important Notes

### Safety Features

- ✅ Only auto-pushes on `main` branch
- ✅ Won't overwrite existing tags
- ✅ Validates version format
- ✅ Graceful error handling
- ✅ Never forces pushes
- ✅ Easy bypass with `--no-verify`

### When Hooks Run

- ✅ Run on: `git commit`
- ✅ Run on: Commits from any tool (CLI, IDE, Claude Code)
- ❌ Don't run on: `git commit --no-verify`
- ❌ Don't run on: `git rebase`, `git cherry-pick`
- ❌ Don't run on: Merge commits (by default)

### Branch-Specific Behavior

The post-commit hook only auto-pushes when on `main` branch. This prevents accidental pushes from feature branches.

## Troubleshooting

### Hooks Not Running

```bash
# Make executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit

# Test
bash .claude/scripts/test_hooks.sh
```

### Push Fails

```bash
# Check remote
git remote -v

# Test connectivity
git fetch origin

# Manual push if needed
git push origin main --tags
```

### Version Issues

```bash
# Show current
python3 .claude/scripts/version_bump.py --show

# Fix manually
python3 .claude/scripts/version_bump.py 0.1.0-alpha.X
```

## Documentation

For more details:

- **Daily use**: Read `.claude/QUICK_REFERENCE.md`
- **Git hooks**: Read `.claude/GIT_HOOKS_GUIDE.md`
- **All options**: Read `.claude/AUTOMATION.md`
- **Commands**: See `.claude/commands/` directory

## Success!

Your project is now fully automated! Every commit will:

1. ✅ Auto-increment the version
2. ✅ Update manifest.json
3. ✅ Create a git tag
4. ✅ Push to Gitea

**No manual version management needed!**

Just code, commit, and everything else happens automatically. 🚀

## Support

If you encounter any issues:

1. Run the test suite: `bash .claude/scripts/test_hooks.sh`
2. Check the documentation files listed above
3. Verify git configuration: `git remote -v`
4. Check hook permissions: `ls -la .git/hooks/`

---

**Setup Date**: 2025-11-10
**Status**: ✅ Complete and tested
**Current Version**: 0.1.0-alpha.1
**Next Version**: 0.1.0-alpha.2 (on next commit)
