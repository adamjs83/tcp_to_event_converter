# Quick Commit with Auto Version Bump

You are helping automate the commit process with automatic version incrementing.

## Your Task

When code changes are made, automatically:
1. Increment the alpha version number
2. Stage all changes
3. Commit with descriptive message including new version
4. Push to Gitea
5. Create and push git tag

## Process

### 1. Check for Changes

```bash
cd "/Users/adamjs83/Library/Mobile Documents/com~apple~CloudDocs/aiworkflows/tcp_to_event_converer"
git status --porcelain
```

If no changes detected, inform user and exit.

### 2. Show Current Status

```bash
# Show what will be committed
git status

# Show current version
python3 .claude/scripts/version_bump.py --show
```

### 3. Increment Version

```bash
# Auto-increment alpha build number
python3 .claude/scripts/version_bump.py
```

This will:
- Read current version from manifest.json
- Increment alpha build number
- Update manifest.json
- Output: "0.1.0-alpha.1 → 0.1.0-alpha.2"

### 4. Stage All Changes

```bash
# Stage everything including the updated manifest.json
git add -A
```

### 5. Create Commit

```bash
# Extract new version for commit message
NEW_VERSION=$(python3 .claude/scripts/version_bump.py --show)

# Commit with descriptive message
git commit -m "$(cat <<EOF
Release version ${NEW_VERSION}

Changes in this release:
- [Claude will list the files that were modified]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 6. Create Git Tag

```bash
NEW_VERSION=$(python3 .claude/scripts/version_bump.py --show)
git tag -a "v${NEW_VERSION}" -m "Release version ${NEW_VERSION}"
```

### 7. Push Everything

```bash
# Push commits
git push origin main

# Push tags
git push origin --tags
```

## Smart Commit Messages

Analyze the changed files and create an intelligent commit message:

- **Python files changed**: "Update core functionality"
- **Config files changed**: "Update configuration"
- **Documentation changed**: "Update documentation"
- **Multiple types**: List all change categories
- **Always include**: File names of what changed

## Example Output

```
Current version: 0.1.0-alpha.1
Bumping to: 0.1.0-alpha.2

Files changed:
- custom_components/tcp_to_event_converter/config_flow.py
- custom_components/tcp_to_event_converter/sensor.py

✓ Version bumped to 0.1.0-alpha.2
✓ manifest.json updated
✓ All changes staged
✓ Committed: "Release version 0.1.0-alpha.2"
✓ Tagged: v0.1.0-alpha.2
✓ Pushed to Gitea

Release complete! 🚀
View at: https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer
```

## Error Handling

### Uncommitted Manifest Changes

If manifest.json was already modified manually:
1. Ask user if version bump script should overwrite it
2. If yes, proceed with auto-increment
3. If no, use existing version and skip version_bump.py

### No Changes to Commit

```
No changes detected in working directory.
Nothing to commit.
```

### Push Failures

If push fails:
1. Show the error
2. Explain likely cause (network, credentials, conflicts)
3. Suggest: "Run 'git push origin main' manually to retry"
4. Note: Local commit and tag were successful

### Already Up to Date

If trying to push but already synced:
```
✓ Everything already up to date with remote
✓ Version: 0.1.0-alpha.2
```

## Flags and Options

Support these options:

```bash
/commit                    # Auto-increment and commit all changes
/commit --no-push         # Commit and tag locally, don't push
/commit --dry-run         # Show what would happen, don't execute
/commit --message "text"  # Use custom commit message
```

## Safety Checks

Before committing:
1. ✓ Verify on main branch
2. ✓ Check no merge conflicts
3. ✓ Validate version format after bump
4. ✓ Ensure manifest.json is valid JSON
5. ✓ Confirm with user if >10 files changed

## Pre-Commit Checklist

- [ ] On main branch
- [ ] No merge conflicts
- [ ] Version format valid
- [ ] manifest.json is valid JSON
- [ ] Git remote configured
- [ ] Changes are intentional

## When to Use This Command

Use `/commit` instead of manual git commands when:
- ✅ You've made code changes and want to release them
- ✅ You want automatic version incrementing
- ✅ You want standardized commit messages
- ✅ You want automated tagging
- ✅ You want one-command push to Gitea

Use manual git commands when:
- ❌ You want to commit without version bump
- ❌ You're working on a feature branch
- ❌ You want granular control over staging
- ❌ You're fixing a commit mistake

## Comparison with /release

| Feature | /commit | /release |
|---------|---------|----------|
| Auto version bump | ✓ | ✓ |
| Stages all changes | ✓ | Only manifest |
| Commits everything | ✓ | Only manifest |
| Creates tag | ✓ | ✓ |
| Pushes to remote | ✓ | ✓ |
| Use case | Daily commits | Formal releases |

## Integration with Development Workflow

Recommended workflow:

1. **Make changes** to code files
2. **Test changes** locally
3. **Run `/commit`** to auto-version, commit, and push
4. **Verify** on Gitea that changes were pushed
5. **Continue development** or deploy

## Post-Commit Actions

After successful commit:
1. Display new version number
2. Show Gitea repository URL
3. List files that were committed
4. Suggest next actions (test, deploy, etc.)

## Configuration

Uses settings from:
- `.claude/settings.local.json` (permissions)
- `.claude/scripts/version_bump.py` (version logic)
- Git config (remote URL, user name/email)

## Limitations

- Only works on main branch (safety feature)
- Requires clean working directory or intentional changes
- Cannot handle merge conflicts automatically
- Requires network connectivity for push
- Cannot undo after push (by design)

## Alternative Workflows

If you need more control:
1. Use `/release` for manifest-only releases
2. Use standard git commands for partial commits
3. Use `git commit -p` for patch-mode staging
4. Use feature branches for experimental work

## Technical Details

### Version Bump Script

The script at `.claude/scripts/version_bump.py`:
- Parses current version from manifest.json
- Validates format: `0.1.0-alpha.X`
- Increments alpha build number
- Writes updated JSON with formatting preserved
- Returns new version for use in commit message

### Commit Message Template

```
Release version {VERSION}

Changes in this release:
- {File 1}: {Description}
- {File 2}: {Description}
...

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Git Tag Format

Annotated tags with format:
```
v{VERSION}
```

Example: `v0.1.0-alpha.2`

## Troubleshooting

### Script Permission Denied

```bash
chmod +x .claude/scripts/version_bump.py
```

### Python Not Found

```bash
# Use python3 explicitly
python3 .claude/scripts/version_bump.py
```

### Git Push Rejected

Usually means:
- Someone else pushed first (need to pull)
- Credentials expired
- Network issue

Solution:
```bash
git pull origin main --rebase
git push origin main
```

## Start Commit Process

When invoked:
1. ✓ Show current status and version
2. ✓ List files that will be committed
3. ✓ Ask for confirmation (unless --yes flag)
4. ✓ Execute version bump
5. ✓ Stage, commit, tag, and push
6. ✓ Display success summary with new version
