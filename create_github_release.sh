#!/bin/bash
# Script to create GitHub Release from existing tag
# Usage: ./create_github_release.sh

set -e

REPO_OWNER="adamjs83"
REPO_NAME="tcp_to_event_converter"
TAG_NAME="v0.1.0-alpha.1"
RELEASE_NAME="TCP to Event Converter v0.1.0-alpha.1"

RELEASE_NOTES="# First Alpha Release

**Status: ALPHA - Experimental software, not production ready**

Breaking changes may occur in future releases.

## Features
- TCP server listening on configurable port
- Converts TCP messages to Home Assistant events
- UI-based configuration through config flow
- Comprehensive error handling and validation
- HACS compatible structure

## Installation

Install via HACS by adding this repository as a custom repository.

## Known Limitations

This is an alpha release. Please report issues on GitHub.

## Documentation

See [README.md](https://github.com/${REPO_OWNER}/${REPO_NAME}/blob/main/README.md) for full documentation."

echo "Creating GitHub Release for ${TAG_NAME}..."

# You need to set GITHUB_TOKEN environment variable
# Create token at: https://github.com/settings/tokens
# Required scopes: repo

if [ -z "$GITHUB_TOKEN" ]; then
    echo "ERROR: GITHUB_TOKEN environment variable not set"
    echo "Create a token at: https://github.com/settings/tokens"
    echo "Then run: export GITHUB_TOKEN='your_token_here'"
    exit 1
fi

# Create the release using GitHub API
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases \
  -d "{
    \"tag_name\": \"${TAG_NAME}\",
    \"name\": \"${RELEASE_NAME}\",
    \"body\": $(echo "$RELEASE_NOTES" | jq -Rs .),
    \"draft\": false,
    \"prerelease\": true
  }"

echo ""
echo "✓ Release created successfully!"
echo "View at: https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/tag/${TAG_NAME}"
