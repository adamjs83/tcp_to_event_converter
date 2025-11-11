#!/bin/bash
#
# Test script for Git hooks
#
# This script tests that the pre-commit and post-commit hooks are working correctly
#

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Git Hooks Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${YELLOW}Project root: $PROJECT_ROOT${NC}"
echo ""

# ========================================
# Test 1: Check Hook Files Exist
# ========================================

echo -e "${BLUE}Test 1: Checking hook files exist...${NC}"

if [ -f ".git/hooks/pre-commit" ]; then
    echo -e "${GREEN}✓ pre-commit hook exists${NC}"
else
    echo -e "${RED}✗ pre-commit hook NOT found${NC}"
    exit 1
fi

if [ -f ".git/hooks/post-commit" ]; then
    echo -e "${GREEN}✓ post-commit hook exists${NC}"
else
    echo -e "${RED}✗ post-commit hook NOT found${NC}"
    exit 1
fi

echo ""

# ========================================
# Test 2: Check Hook Permissions
# ========================================

echo -e "${BLUE}Test 2: Checking hook permissions...${NC}"

if [ -x ".git/hooks/pre-commit" ]; then
    echo -e "${GREEN}✓ pre-commit is executable${NC}"
else
    echo -e "${RED}✗ pre-commit is NOT executable${NC}"
    echo "Run: chmod +x .git/hooks/pre-commit"
    exit 1
fi

if [ -x ".git/hooks/post-commit" ]; then
    echo -e "${GREEN}✓ post-commit is executable${NC}"
else
    echo -e "${RED}✗ post-commit is NOT executable${NC}"
    echo "Run: chmod +x .git/hooks/post-commit"
    exit 1
fi

echo ""

# ========================================
# Test 3: Check Version Script
# ========================================

echo -e "${BLUE}Test 3: Checking version script...${NC}"

if [ -f ".claude/scripts/version_bump.py" ]; then
    echo -e "${GREEN}✓ version_bump.py exists${NC}"
else
    echo -e "${RED}✗ version_bump.py NOT found${NC}"
    exit 1
fi

# Test that script can show version
CURRENT_VERSION=$(python3 .claude/scripts/version_bump.py --show 2>&1)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Version script works (current: $CURRENT_VERSION)${NC}"
else
    echo -e "${RED}✗ Version script failed: $CURRENT_VERSION${NC}"
    exit 1
fi

echo ""

# ========================================
# Test 4: Check Manifest File
# ========================================

echo -e "${BLUE}Test 4: Checking manifest.json...${NC}"

MANIFEST_PATH="custom_components/tcp_to_event_converter/manifest.json"

if [ -f "$MANIFEST_PATH" ]; then
    echo -e "${GREEN}✓ manifest.json exists${NC}"
else
    echo -e "${RED}✗ manifest.json NOT found${NC}"
    exit 1
fi

# Validate JSON format
if python3 -m json.tool "$MANIFEST_PATH" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ manifest.json is valid JSON${NC}"
else
    echo -e "${RED}✗ manifest.json is INVALID JSON${NC}"
    exit 1
fi

# Check version format
VERSION=$(python3 .claude/scripts/version_bump.py --show)
if [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+-alpha\.[0-9]+$ ]]; then
    echo -e "${GREEN}✓ Version format is valid: $VERSION${NC}"
else
    echo -e "${RED}✗ Version format is invalid: $VERSION${NC}"
    exit 1
fi

echo ""

# ========================================
# Test 5: Check Git Configuration
# ========================================

echo -e "${BLUE}Test 5: Checking git configuration...${NC}"

# Check we're in a git repo
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${GREEN}✓ In a git repository${NC}"
else
    echo -e "${RED}✗ NOT in a git repository${NC}"
    exit 1
fi

# Check remote
if git remote | grep -q "origin"; then
    REMOTE_URL=$(git remote get-url origin)
    echo -e "${GREEN}✓ Remote 'origin' configured: $REMOTE_URL${NC}"
else
    echo -e "${RED}✗ Remote 'origin' not configured${NC}"
    exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "${GREEN}✓ Current branch: $CURRENT_BRANCH${NC}"

echo ""

# ========================================
# Test 6: Simulate Pre-commit Hook
# ========================================

echo -e "${BLUE}Test 6: Simulating pre-commit hook...${NC}"

# Save current version
ORIGINAL_VERSION=$(python3 .claude/scripts/version_bump.py --show)
echo "Original version: $ORIGINAL_VERSION"

# Run version bump (dry run by showing what would happen)
echo "Testing version increment..."
TEST_OUTPUT=$(python3 .claude/scripts/version_bump.py 2>&1)

# Get new version
NEW_VERSION=$(python3 .claude/scripts/version_bump.py --show)
echo "After increment: $NEW_VERSION"

if [ "$NEW_VERSION" != "$ORIGINAL_VERSION" ]; then
    echo -e "${GREEN}✓ Version increment works${NC}"

    # Restore original version
    echo "Restoring original version..."
    python3 .claude/scripts/version_bump.py "$ORIGINAL_VERSION" > /dev/null 2>&1
    RESTORED=$(python3 .claude/scripts/version_bump.py --show)

    if [ "$RESTORED" = "$ORIGINAL_VERSION" ]; then
        echo -e "${GREEN}✓ Version restored to $ORIGINAL_VERSION${NC}"
    else
        echo -e "${RED}✗ Failed to restore version (now: $RESTORED, expected: $ORIGINAL_VERSION)${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Version did not increment${NC}"
    exit 1
fi

echo ""

# ========================================
# Test 7: Check Hook Configuration
# ========================================

echo -e "${BLUE}Test 7: Checking hook configuration...${NC}"

# Check pre-commit hook references version script
if grep -q "version_bump.py" .git/hooks/pre-commit; then
    echo -e "${GREEN}✓ pre-commit references version_bump.py${NC}"
else
    echo -e "${RED}✗ pre-commit does not reference version_bump.py${NC}"
    exit 1
fi

# Check post-commit hook references tagging
if grep -q "git tag" .git/hooks/post-commit; then
    echo -e "${GREEN}✓ post-commit includes tagging logic${NC}"
else
    echo -e "${RED}✗ post-commit missing tagging logic${NC}"
    exit 1
fi

# Check post-commit hook references pushing
if grep -q "git push" .git/hooks/post-commit; then
    echo -e "${GREEN}✓ post-commit includes push logic${NC}"
else
    echo -e "${RED}✗ post-commit missing push logic${NC}"
    exit 1
fi

echo ""

# ========================================
# Summary
# ========================================

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}All tests passed! ✓${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Current configuration:${NC}"
echo "  Version: $ORIGINAL_VERSION"
echo "  Branch: $CURRENT_BRANCH"
echo "  Remote: $(git remote get-url origin)"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Make code changes"
echo "2. Run: git add -A"
echo "3. Run: git commit -m 'Your message'"
echo "4. Hooks will automatically:"
echo "   - Increment version"
echo "   - Update manifest.json"
echo "   - Create git tag"
echo "   - Push to Gitea"
echo ""
echo -e "${YELLOW}To test with a real commit:${NC}"
echo "  echo '# Test' >> README.md"
echo "  git add README.md"
echo "  git commit -m 'Test automated versioning'"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo "  Read: .claude/GIT_HOOKS_GUIDE.md"
echo ""

exit 0
