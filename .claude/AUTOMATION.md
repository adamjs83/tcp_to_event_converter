# Claude Code Automation Documentation

This document describes the automated workflows configured for the TCP to Event Converter project.

## Overview

The project is configured with automated version management and release workflows that handle:
1. Automatic version incrementing using semantic versioning (alpha builds)
2. Updating manifest.json with new version numbers
3. Git commit creation with descriptive messages
4. Git tagging for releases
5. Automatic push to Gitea remote repository

## Version Format

The project uses semantic versioning with alpha builds:
- **Format**: `0.1.0-alpha.X`
- **Increment**: Only the alpha build number (X) is automatically incremented
- **Example**: `0.1.0-alpha.1` → `0.1.0-alpha.2` → `0.1.0-alpha.3`

## Automated Release Process

### Using the `/release` Command

The primary way to create a release is using the `/release` slash command:

```bash
/release                    # Auto-increment alpha version
/release 0.1.0-alpha.5     # Set specific version
/release --skip-push       # Commit and tag but don't push
```

### What Happens During a Release

1. **Version Check**: Reads current version from `manifest.json`
2. **Version Increment**: Calculates next alpha build number
3. **Git Status Check**: Verifies repository state and current branch
4. **Manifest Update**: Updates version in `manifest.json`
5. **Git Commit**: Creates commit with descriptive message
6. **Git Tag**: Creates annotated tag for the version
7. **Push to Gitea**: Pushes commits and tags to remote

### Release Command Details

The `/release` command is defined in:
```
.claude/commands/release.md
```

Key features:
- Validates version format
- Ensures clean working directory (or only intended changes)
- Confirms user is on main branch
- Creates descriptive commit messages
- Provides detailed feedback at each step
- Handles errors gracefully

## Version Management Script

### Location
```
.claude/scripts/version_bump.py
```

### Usage

```bash
# Show current version
python3 .claude/scripts/version_bump.py --show

# Auto-increment alpha build
python3 .claude/scripts/version_bump.py

# Set specific version
python3 .claude/scripts/version_bump.py 0.1.0-alpha.5

# Show help
python3 .claude/scripts/version_bump.py --help
```

### Script Features

- **Automatic Discovery**: Finds manifest.json automatically
- **Version Parsing**: Validates version format
- **Safe Updates**: Preserves JSON formatting
- **Error Handling**: Clear error messages for invalid versions
- **Scriptable**: Returns parseable output for automation

### Example Output

```bash
$ python3 .claude/scripts/version_bump.py
0.1.0-alpha.1 → 0.1.0-alpha.2
Updated /path/to/custom_components/tcp_to_event_converter/manifest.json
```

## Git Configuration

### Remote Repository
- **URL**: `https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer.git`
- **Remote Name**: `origin`
- **Default Branch**: `main`

### Commit Message Format

```
Release version 0.1.0-alpha.X

- Automated version bump
- Updated manifest.json with new version number

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Tag Format

Tags are created as annotated tags:
```bash
git tag -a "v0.1.0-alpha.X" -m "Release version 0.1.0-alpha.X"
```

## Permissions Configuration

The following permissions are configured in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(git push:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git tag:*)",
      "Bash(git status:*)",
      "Bash(git branch:*)",
      "Bash(git remote:*)",
      "Bash(python:*::*)",
      "Bash(python:*)",
      "Bash(cat:*)",
      "Bash(chmod:*)",
      "Bash(mkdir:*)",
      "Bash(git mv:*)",
      "Bash(tree:*)"
    ]
  }
}
```

These permissions allow Claude Code to:
- Run git commands for version control
- Execute Python scripts for version management
- Read files for version checking
- Create and modify files as needed

## Workflow Examples

### Standard Release

```
User: /release
Claude: Bumping version from 0.1.0-alpha.1 to 0.1.0-alpha.2...
        ✓ Version bumped in manifest.json
        ✓ Changes committed
        ✓ Git tag created: v0.1.0-alpha.2
        ✓ Pushed to Gitea
```

### Custom Version Release

```
User: /release 0.1.0-alpha.10
Claude: Setting version to 0.1.0-alpha.10...
        ✓ Version set in manifest.json
        ✓ Changes committed
        ✓ Git tag created: v0.1.0-alpha.10
        ✓ Pushed to Gitea
```

### Local Release (No Push)

```
User: /release --skip-push
Claude: Bumping version from 0.1.0-alpha.1 to 0.1.0-alpha.2...
        ✓ Version bumped in manifest.json
        ✓ Changes committed
        ✓ Git tag created: v0.1.0-alpha.2
        ⚠ Skipped push (--skip-push flag)
```

## Safety Features

### Pre-Release Checks

Before executing a release:
1. Verify git working directory state
2. Confirm current branch is `main`
3. Validate current version format
4. Check Gitea remote configuration
5. Request user confirmation (unless `--yes` flag used)

### Error Handling

The release process will abort if:
- Working directory has unexpected uncommitted changes
- Not on the main branch
- Version format is invalid
- Git remote is not configured correctly
- Network issues prevent pushing

### Rollback

If a release fails partway through:
1. Local commits remain in git history
2. Tags can be deleted with `git tag -d v0.1.0-alpha.X`
3. Previous version can be restored manually
4. No force pushes are ever used

## Manual Version Management

If you need to manage versions manually:

### Update Version in manifest.json

Edit the file directly:
```bash
/Users/adamjs83/Library/Mobile Documents/com~apple~CloudDocs/aiworkflows/tcp_to_event_converer/custom_components/tcp_to_event_converter/manifest.json
```

Change the version field:
```json
{
  "version": "0.1.0-alpha.X"
}
```

### Manual Git Operations

```bash
# Commit changes
git add custom_components/tcp_to_event_converter/manifest.json
git commit -m "Release version 0.1.0-alpha.X"

# Create tag
git tag -a "v0.1.0-alpha.X" -m "Release version 0.1.0-alpha.X"

# Push to Gitea
git push origin main
git push origin --tags
```

## Troubleshooting

### Version Script Not Found

```bash
# Make script executable
chmod +x .claude/scripts/version_bump.py

# Or run with python3 explicitly
python3 .claude/scripts/version_bump.py
```

### Git Push Fails

```bash
# Check remote configuration
git remote -v

# Verify credentials
git push origin main --dry-run

# Check network connectivity
ping gitea.ajsventures.us
```

### Invalid Version Format

Ensure version follows pattern: `MAJOR.MINOR.PATCH-alpha.BUILD`
- Example: `0.1.0-alpha.1`
- Not: `0.1.0`, `v0.1.0-alpha.1`, `0.1.0-alpha1`

## File Structure

```
.claude/
├── commands/
│   ├── release.md          # /release slash command definition
│   ├── analyze.md          # Code analysis command
│   ├── review.md           # Code review command
│   └── test.md             # Testing command
├── scripts/
│   └── version_bump.py     # Version management utility
├── settings.local.json     # Permissions and configuration
├── system_prompt.md        # Claude Code system instructions
├── README.md               # General Claude Code documentation
└── AUTOMATION.md           # This file
```

## Best Practices

### When to Release

Create a new release when:
- New features are added
- Bugs are fixed
- Configuration changes are made
- Documentation is updated (minor changes)

### Version Numbering Strategy

- **0.1.0-alpha.1**: Initial alpha release
- **0.1.0-alpha.2+**: Incremental alpha builds
- **0.1.0-beta.1**: When ready for beta testing (manual bump)
- **0.1.0**: First stable release (manual bump)
- **0.2.0**: Minor version for new features
- **1.0.0**: Major version for breaking changes

### Git Workflow

1. Make changes to code
2. Test changes locally
3. Run `/release` to create new version
4. Verify in Gitea that changes were pushed
5. Update GitHub mirror if applicable

## Integration with CI/CD

Future enhancements could include:
- Automatic testing before release
- GitHub Actions integration
- Automated changelog generation
- Release notes creation
- Docker image building
- Home Assistant Community Store (HACS) integration

## Related Commands

- `/analyze` - Comprehensive code analysis
- `/review` - Code review for changes
- `/test` - Run tests (if configured)

## Support

For issues with the automation:
1. Check this documentation
2. Review `.claude/commands/release.md` for command details
3. Examine `.claude/scripts/version_bump.py` for script logic
4. Verify permissions in `.claude/settings.local.json`
5. Check git configuration with `git remote -v`

## Git Hooks - Automatic Versioning on Every Commit

**NEW**: This project now includes Git hooks that automatically handle versioning!

### What Happens When You Commit

Every time you run `git commit`, the following happens automatically:

1. **Pre-commit Hook**:
   - Increments alpha version (0.1.0-alpha.1 → 0.1.0-alpha.2)
   - Updates manifest.json with new version
   - Stages the updated manifest.json

2. **Post-commit Hook**:
   - Creates annotated git tag (e.g., v0.1.0-alpha.2)
   - Pushes commit to Gitea (origin/main)
   - Pushes tag to Gitea

### Quick Start with Hooks

```bash
# Normal workflow - hooks do everything automatically
git add -A
git commit -m "Add new feature"

# Output will show:
# 🔄 Pre-commit hook: Auto-versioning...
# ✓ 0.1.0-alpha.1 → 0.1.0-alpha.2
# 🚀 Post-commit hook: Processing release...
# ✓ Created tag: v0.1.0-alpha.2
# ✓ Pushed to Gitea
# 🎉 Release 0.1.0-alpha.2 published!

# To bypass hooks (work-in-progress commits)
git commit --no-verify -m "WIP: Experimental changes"
```

### Hook Configuration

**Pre-commit hook**: `.git/hooks/pre-commit`
- Automatically increments version
- Updates manifest.json
- Stages the changes

**Post-commit hook**: `.git/hooks/post-commit`
- Creates git tags
- Pushes to remote
- Configurable via variables in the hook file

### Disable Auto-Push

Edit `.git/hooks/post-commit` and change:
```bash
AUTO_PUSH_ENABLED=false  # Commit locally only
AUTO_TAG_ENABLED=false   # Skip tagging
```

### Documentation

For complete details, see: `.claude/GIT_HOOKS_GUIDE.md`

### Test Hooks

```bash
# Run test suite to verify hooks are working
bash .claude/scripts/test_hooks.sh
```

## Automation Options Comparison

### Option 1: Git Hooks (Automatic - NEW!)

**Best for**: Daily development workflow

```bash
# Just commit - everything else is automatic
git add -A
git commit -m "Fix bug"
# ✓ Auto-versions, tags, and pushes
```

**Pros**:
- ✅ Truly automatic on every commit
- ✅ Works with standard git commands
- ✅ Works outside Claude Code
- ✅ No manual intervention needed

**Cons**:
- ⚠️ Every commit creates a version and push
- ⚠️ Requires `--no-verify` for WIP commits

### Option 2: Claude `/commit` Command

**Best for**: Claude Code users who want automation with control

```bash
/commit                    # Auto-version and commit all changes
/commit --no-push         # Commit locally only
/commit --dry-run         # Preview what will happen
```

**Pros**:
- ✅ More control over what gets committed
- ✅ Smart commit messages
- ✅ Shows preview before executing

**Cons**:
- ⚠️ Requires manual invocation of `/commit`
- ⚠️ Only works in Claude Code

### Option 3: Manual `/release` Command

**Best for**: Formal, planned releases

```bash
/release                   # Auto-increment
/release 0.1.0-alpha.5    # Set specific version
/release --skip-push      # Local only
```

**Pros**:
- ✅ Full control over releases
- ✅ Can set custom versions
- ✅ Best for major milestones

**Cons**:
- ⚠️ Requires manual invocation
- ⚠️ More steps for routine commits

## Recommended Workflow

**For daily development** (use Git hooks):
```bash
# Make changes
vim custom_components/tcp_to_event_converter/sensor.py

# Commit (hooks auto-version and push)
git add -A
git commit -m "Fix sensor parsing"
```

**For work-in-progress**:
```bash
# Bypass hooks for temporary commits
git commit --no-verify -m "WIP: Experimenting"
```

**For formal releases**:
```bash
# Use /release for specific versions
/release 0.1.0-beta.1
```

## Related Commands

- `/commit` - Claude Code assisted commit with auto-versioning
- `/release` - Manual release with custom version control
- `/analyze` - Comprehensive code analysis
- `/review` - Code review for changes
- `/test` - Run tests (if configured)

## Support

For issues with the automation:
1. Check this documentation
2. Review `.claude/GIT_HOOKS_GUIDE.md` for hook details
3. Review `.claude/commands/release.md` for command details
4. Examine `.claude/scripts/version_bump.py` for script logic
5. Verify permissions in `.claude/settings.local.json`
6. Check git configuration with `git remote -v`
7. Run test suite: `bash .claude/scripts/test_hooks.sh`

## Version History

- **2025-11-10**: Git hooks automation added
  - Created pre-commit hook for auto-versioning
  - Created post-commit hook for auto-tagging and pushing
  - Added `/commit` Claude Code command
  - Created comprehensive test suite
  - Added Git Hooks Guide documentation

- **2025-01-10**: Initial automation setup
  - Created `/release` command
  - Implemented `version_bump.py` script
  - Configured permissions for automated git operations
  - Documented automation workflows
