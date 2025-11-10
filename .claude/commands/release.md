# Release New Version

You are automating the release process for the TCP to Event Converter Home Assistant integration.

## Your Task

Automatically increment the alpha version number, update manifest.json, commit changes, and push to Gitea.

## Version Format

The project uses semantic versioning with alpha builds:
- Format: `0.1.0-alpha.X`
- Only increment the alpha build number (X)
- Example: `0.1.0-alpha.1` → `0.1.0-alpha.2`

## Release Process

Follow these steps in order:

### 1. Read Current Version

```bash
# Read the current version from manifest.json
cat custom_components/tcp_to_event_converter/manifest.json
```

### 2. Calculate Next Version

Extract the current alpha build number and increment it:
- Current: `0.1.0-alpha.1`
- Next: `0.1.0-alpha.2`

### 3. Check Git Status

```bash
# Ensure we're on the main branch and check for uncommitted changes
git status
git branch --show-current
```

### 4. Update manifest.json

Use the Edit tool to update the version field in:
`/Users/adamjs83/Library/Mobile Documents/com~apple~CloudDocs/aiworkflows/tcp_to_event_converer/custom_components/tcp_to_event_converter/manifest.json`

### 5. Commit and Tag

```bash
# Stage the manifest.json file
git add custom_components/tcp_to_event_converter/manifest.json

# Commit with a descriptive message
git commit -m "Release version 0.1.0-alpha.X

- Automated version bump
- Updated manifest.json with new version number"

# Create a git tag for this version
git tag -a "v0.1.0-alpha.X" -m "Release version 0.1.0-alpha.X"
```

### 6. Push to Gitea

```bash
# Push the commit and tags to the Gitea remote
git push origin main
git push origin --tags
```

## Error Handling

If any step fails:
1. Report the error clearly
2. Do NOT continue to next steps
3. Provide guidance on how to fix the issue
4. Do NOT leave the repository in an inconsistent state

Common issues:
- **Uncommitted changes**: Stash or commit them first
- **Not on main branch**: Switch to main branch
- **Push fails**: Check network connection and credentials
- **Merge conflicts**: User must resolve manually

## Success Confirmation

After successful release, provide a summary:

```
✓ Version bumped: 0.1.0-alpha.X → 0.1.0-alpha.Y
✓ manifest.json updated
✓ Changes committed with message: "Release version 0.1.0-alpha.Y"
✓ Git tag created: v0.1.0-alpha.Y
✓ Pushed to Gitea: https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer.git
```

## Pre-Release Checklist

Before executing the release, verify:

- [ ] Git working directory is clean or only has intended changes
- [ ] Currently on the main branch
- [ ] Current version number is valid format (0.1.0-alpha.X)
- [ ] Gitea remote is configured correctly
- [ ] User has confirmed they want to proceed with release

## Additional Parameters

The user may specify:
- **Custom version**: Override automatic increment with specific version
- **Commit message**: Use custom commit message
- **Skip push**: Commit and tag but don't push (for testing)

## Example Usage

```bash
# User runs: /release
# Result: Automatic bump from 0.1.0-alpha.1 to 0.1.0-alpha.2

# User runs: /release 0.1.0-alpha.5
# Result: Set version to 0.1.0-alpha.5 (custom version)

# User runs: /release --skip-push
# Result: Commit and tag locally but don't push to Gitea
```

## Git Configuration

The Gitea remote URL is:
- URL: `https://gitea.ajsventures.us/adamjs83/tcp_to_event_converer.git`
- Remote name: `origin`
- Default branch: `main`

## Post-Release Actions

After successful release:
1. Inform user of new version number
2. Provide link to Gitea repository
3. Suggest running tests if available
4. Ask if user wants to create a GitHub release/changelog

## Safety Features

- Never force push
- Never rewrite published history
- Always create tags for releases
- Provide clear error messages
- Allow user to abort before pushing

## Start Release Process

When this command is invoked:
1. Ask user to confirm release (unless they used --yes flag)
2. Show current version and what it will become
3. Execute release steps systematically
4. Provide clear feedback at each step
5. Summarize results at the end
