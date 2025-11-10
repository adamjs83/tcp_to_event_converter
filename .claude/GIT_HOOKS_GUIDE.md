# Git Hooks Automation Guide

This project uses Git hooks to automatically manage versioning and releases whenever you commit changes.

## What Happens Automatically

When you run `git commit`:

1. **Pre-commit Hook** (`pre-commit`)
   - ✅ Automatically increments alpha version (0.1.0-alpha.1 → 0.1.0-alpha.2)
   - ✅ Updates `manifest.json` with new version
   - ✅ Stages the updated manifest.json
   - ✅ Allows commit to proceed

2. **Post-commit Hook** (`post-commit`)
   - ✅ Creates annotated git tag (e.g., `v0.1.0-alpha.2`)
   - ✅ Pushes commit to Gitea (`origin/main`)
   - ✅ Pushes tag to Gitea
   - ✅ Displays success message

## Quick Start

### Normal Workflow

```bash
# 1. Make your code changes
vim custom_components/tcp_to_event_converter/config_flow.py

# 2. Stage your changes
git add -A

# 3. Commit (hooks will automatically version, tag, and push)
git commit -m "Add new feature"

# Output:
# 🔄 Pre-commit hook: Auto-versioning...
# Current version: 0.1.0-alpha.1
# ✓ 0.1.0-alpha.1 → 0.1.0-alpha.2
# ✓ Staged updated manifest.json with version 0.1.0-alpha.2
# [main abc1234] Add new feature
# 🚀 Post-commit hook: Processing release...
# ✓ Created tag: v0.1.0-alpha.2
# ✓ Pushed commit to origin/main
# ✓ Pushed tag to origin
# 🎉 Release 0.1.0-alpha.2 published to Gitea!
```

### Bypass Automation (Manual Control)

```bash
# Skip ALL hooks (no auto-version, no auto-push)
git commit --no-verify -m "WIP: Work in progress"

# Then manually push later
git push origin main
```

## Hook Configuration

### Pre-commit Hook

**Location**: `.git/hooks/pre-commit`

**What it does**:
- Runs Python script: `.claude/scripts/version_bump.py`
- Reads current version from `manifest.json`
- Increments alpha build number
- Writes new version back to `manifest.json`
- Stages the updated file

**To disable**:
```bash
# Rename or remove the hook
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
```

### Post-commit Hook

**Location**: `.git/hooks/post-commit`

**What it does**:
- Creates annotated tag: `v{VERSION}`
- Pushes to remote: `origin/main`
- Pushes tags to remote

**Configuration Variables** (edit the hook file):
```bash
# Set to "false" to disable automatic pushing
AUTO_PUSH_ENABLED=true

# Set to "false" to disable automatic tagging
AUTO_TAG_ENABLED=true

# Remote name
REMOTE_NAME="origin"

# Branch name
BRANCH_NAME="main"
```

**To disable auto-push but keep tagging**:
```bash
# Edit .git/hooks/post-commit
vim .git/hooks/post-commit

# Change this line:
AUTO_PUSH_ENABLED=false
```

## Workflow Examples

### Example 1: Simple Bug Fix

```bash
# Fix a bug
vim custom_components/tcp_to_event_converter/sensor.py

# Commit (auto-versions and pushes)
git add -A
git commit -m "Fix sensor data parsing bug"

# Result:
# - Version: 0.1.0-alpha.1 → 0.1.0-alpha.2
# - Tag: v0.1.0-alpha.2
# - Pushed to Gitea automatically
```

### Example 2: Multiple File Changes

```bash
# Modify multiple files
vim custom_components/tcp_to_event_converter/config_flow.py
vim custom_components/tcp_to_event_converter/sensor.py
vim README.md

# Stage and commit everything
git add -A
git commit -m "Refactor configuration and update docs"

# Result:
# - All files committed together
# - Version incremented once
# - Single tag created
# - Everything pushed automatically
```

### Example 3: Work in Progress (No Auto-Push)

```bash
# Make experimental changes
vim custom_components/tcp_to_event_converter/experimental.py

# Commit locally without pushing
git add -A
git commit --no-verify -m "WIP: Experimental feature"

# Continue working...
# When ready, manually push:
git push origin main
```

### Example 4: Quick Documentation Update

```bash
# Update docs
vim README.md

# Commit (still auto-versions because it's a release)
git add README.md
git commit -m "Update installation instructions"

# Result:
# - Version: 0.1.0-alpha.5 → 0.1.0-alpha.6
# - Even docs changes get versioned
```

## Version Management

### Version Format

- **Pattern**: `MAJOR.MINOR.PATCH-alpha.BUILD`
- **Example**: `0.1.0-alpha.1`
- **Auto-increment**: Only BUILD number increases

### Version Progression

```
0.1.0-alpha.1  (Initial)
0.1.0-alpha.2  (Auto-incremented on commit)
0.1.0-alpha.3  (Auto-incremented on commit)
...
0.1.0-alpha.10
0.1.0-alpha.11
```

### Manual Version Control

If you need to manually set a specific version:

```bash
# Set custom version
python3 .claude/scripts/version_bump.py 0.1.0-alpha.25

# Then commit
git add custom_components/tcp_to_event_converter/manifest.json
git commit -m "Bump to alpha.25 for testing"
```

## Git Tags

### Tag Format

All tags are **annotated tags** with the format: `v{VERSION}`

Examples:
- `v0.1.0-alpha.1`
- `v0.1.0-alpha.2`
- `v0.1.0-alpha.10`

### View Tags

```bash
# List all tags
git tag -l

# Show tag details
git show v0.1.0-alpha.2

# List tags with commit messages
git tag -l -n
```

### Delete Tag (if needed)

```bash
# Delete local tag
git tag -d v0.1.0-alpha.2

# Delete remote tag
git push origin :refs/tags/v0.1.0-alpha.2
```

## Troubleshooting

### Hook Doesn't Run

**Problem**: Hooks don't execute when committing

**Solutions**:
```bash
# Check if hooks are executable
ls -la .git/hooks/pre-commit
ls -la .git/hooks/post-commit

# Make them executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit

# Verify they exist
cat .git/hooks/pre-commit
cat .git/hooks/post-commit
```

### Version Bump Fails

**Problem**: Pre-commit hook fails to increment version

**Solutions**:
```bash
# Check if Python script exists
ls -la .claude/scripts/version_bump.py

# Test script manually
python3 .claude/scripts/version_bump.py --show

# Check manifest.json format
cat custom_components/tcp_to_event_converter/manifest.json | python3 -m json.tool
```

### Push Fails

**Problem**: Post-commit hook cannot push to Gitea

**Possible Causes**:
- Network connectivity issue
- Authentication failure
- Remote repository not configured
- Merge conflict on remote

**Solutions**:
```bash
# Check remote configuration
git remote -v

# Test connectivity
ping gitea.ajsventures.us

# Try manual push
git push origin main --dry-run

# Pull first if behind
git pull origin main --rebase
git push origin main
```

### Duplicate Version Numbers

**Problem**: Version didn't increment, using same number

**Cause**: manifest.json wasn't properly updated on previous commit

**Solution**:
```bash
# Check current version
python3 .claude/scripts/version_bump.py --show

# Manually increment
python3 .claude/scripts/version_bump.py

# Verify it worked
cat custom_components/tcp_to_event_converter/manifest.json
```

### Hook Runs on Wrong Branch

**Problem**: Hook auto-pushes on feature branch

**Solution**: Post-commit hook only runs on `main` branch by default.
If you need to change this:

```bash
# Edit hook
vim .git/hooks/post-commit

# Find this line:
BRANCH_NAME="main"

# Change to your branch name or disable the check
```

## Advanced Configuration

### Disable Auto-Push (Keep Local Only)

```bash
# Edit post-commit hook
vim .git/hooks/post-commit

# Change this line:
AUTO_PUSH_ENABLED=false

# Now commits will version and tag locally, but not push
```

### Disable Auto-Tagging

```bash
# Edit post-commit hook
vim .git/hooks/post-commit

# Change this line:
AUTO_TAG_ENABLED=false

# Now commits will push but not create tags
```

### Custom Remote or Branch

```bash
# Edit post-commit hook
vim .git/hooks/post-commit

# Change these lines:
REMOTE_NAME="origin"      # Change to your remote name
BRANCH_NAME="main"        # Change to your branch name
```

### Completely Disable Automation

```bash
# Rename hooks to disable them
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
mv .git/hooks/post-commit .git/hooks/post-commit.disabled

# Re-enable later
mv .git/hooks/pre-commit.disabled .git/hooks/pre-commit
mv .git/hooks/post-commit.disabled .git/hooks/post-commit
```

## Integration with Claude Code

### Using Claude Code Commands

You can still use Claude Code commands alongside hooks:

```bash
# Use /commit command (Claude Code)
/commit

# Or use regular git with hooks
git add -A && git commit -m "message"
```

Both approaches work! The hooks enhance regular git commands.

### Using /release Command

The `/release` command still works and complements the hooks:

```bash
# Manual release with custom version
/release 0.1.0-alpha.15

# Regular commit with auto-version
git commit -m "Fix bug"  # Auto-increments to next version
```

## Best Practices

### When to Use Hooks

✅ **Use automated hooks for**:
- Regular development commits
- Bug fixes
- Feature additions
- Documentation updates
- Configuration changes

❌ **Bypass hooks for**:
- Work-in-progress commits (`git commit --no-verify`)
- Temporary/experimental changes
- Commits you don't want to push yet
- Merge commits
- Rebase operations

### Commit Message Guidelines

Since every commit creates a release:

```bash
# Good commit messages (descriptive)
git commit -m "Add TCP timeout configuration option"
git commit -m "Fix null pointer in event parser"
git commit -m "Update README with new installation steps"

# Less useful (too vague)
git commit -m "Fix bug"
git commit -m "Update"
git commit -m "WIP"
```

### Version Strategy

- **Alpha builds**: Continuous development (current stage)
- **Manual bump to beta**: When ready for wider testing
- **Manual bump to stable**: When production-ready

```bash
# When ready for beta (manual)
python3 .claude/scripts/version_bump.py 0.1.0-beta.1

# When ready for stable (manual)
python3 .claude/scripts/version_bump.py 0.1.0
```

## Safety Features

The hooks include several safety measures:

1. **Non-destructive**: Never forces pushes or rewrites history
2. **Validation**: Checks version format before committing
3. **Error handling**: Graceful failures with helpful messages
4. **Branch check**: Only auto-pushes on main branch
5. **Existing tag check**: Won't overwrite existing tags
6. **Bypass option**: `--no-verify` flag always available

## Monitoring Releases

### View Recent Releases

```bash
# Show recent tags
git tag -l --sort=-version:refname | head -10

# Show commits with versions
git log --oneline --decorate | head -10

# View specific release
git show v0.1.0-alpha.5
```

### Check Gitea

Visit your repository:
https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer

- **Commits**: See all commits pushed
- **Tags**: View all release tags
- **Releases**: Create formal releases from tags

## Backup and Recovery

### Backup Hook Configuration

```bash
# Save your hooks
cp .git/hooks/pre-commit ~/backup-pre-commit
cp .git/hooks/post-commit ~/backup-post-commit
```

### Restore Hooks

```bash
# Restore from backup
cp ~/backup-pre-commit .git/hooks/pre-commit
cp ~/backup-post-commit .git/hooks/post-commit
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit
```

### Hook Source Control

**Note**: Hooks in `.git/hooks/` are NOT version controlled by git.

To share hooks with other developers:

```bash
# Copy to versioned location
cp .git/hooks/pre-commit .claude/hooks/pre-commit
cp .git/hooks/post-commit .claude/hooks/post-commit

# Add to git
git add .claude/hooks/
git commit -m "Add git hooks for automation"
```

## Testing Hooks

### Test Pre-commit Hook

```bash
# Create a test file
echo "test" > test.txt
git add test.txt

# Commit (hook will run)
git commit -m "Test commit"

# Check if version was bumped
python3 .claude/scripts/version_bump.py --show

# Remove test file
git rm test.txt
git commit -m "Remove test file"
```

### Test Post-commit Hook

```bash
# Make a trivial change
echo "# Test" >> README.md
git add README.md

# Commit and watch for push
git commit -m "Test hook"

# Verify tag was created
git tag -l | tail -1

# Verify it was pushed
git ls-remote --tags origin | tail -1
```

### Dry-Run Testing

To test without actually pushing:

```bash
# Edit post-commit hook temporarily
vim .git/hooks/post-commit

# Change:
AUTO_PUSH_ENABLED=false

# Test commit
git add . && git commit -m "Test"

# Change back:
AUTO_PUSH_ENABLED=true
```

## Documentation Files

- `.claude/GIT_HOOKS_GUIDE.md` - This file (comprehensive guide)
- `.claude/AUTOMATION.md` - Claude Code automation overview
- `.claude/commands/commit.md` - Claude `/commit` command
- `.claude/commands/release.md` - Claude `/release` command

## Summary

**Automated workflow**:
```bash
# 1. Make changes
vim some_file.py

# 2. Commit (everything else is automatic)
git add -A
git commit -m "Descriptive message"

# Result:
# ✓ Version auto-incremented
# ✓ manifest.json updated
# ✓ Git tag created
# ✓ Pushed to Gitea
```

**Manual override**:
```bash
# Bypass all automation
git commit --no-verify -m "WIP"
```

The hooks make your workflow simpler while maintaining full control when needed!
