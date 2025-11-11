#!/usr/bin/env python3
"""
Version Bump Utility for TCP to Event Converter

This script handles automatic version incrementing for the Home Assistant integration.
It supports semantic versioning with alpha builds: 0.1.0-alpha.X

Usage:
    python version_bump.py                    # Auto-increment alpha build
    python version_bump.py 0.1.0-alpha.5     # Set specific version
    python version_bump.py --show            # Show current version
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional, Tuple


def find_manifest() -> Path:
    """Find the manifest.json file in the project."""
    # Start from script location and search for manifest
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    manifest_path = project_root / "custom_components" / "tcp_to_event_converter" / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest.json not found at {manifest_path}")

    return manifest_path


def parse_version(version_string: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Parse version string into components.

    Args:
        version_string: Version in format "0.1.0-alpha.X"

    Returns:
        Tuple of (major, minor, patch, alpha) or None if invalid
    """
    pattern = r'^(\d+)\.(\d+)\.(\d+)-alpha\.(\d+)$'
    match = re.match(pattern, version_string)

    if match:
        return tuple(map(int, match.groups()))
    return None


def format_version(major: int, minor: int, patch: int, alpha: int) -> str:
    """Format version components into version string."""
    return f"{major}.{minor}.{patch}-alpha.{alpha}"


def read_current_version(manifest_path: Path) -> str:
    """Read current version from manifest.json."""
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    return manifest.get('version', '')


def write_version(manifest_path: Path, new_version: str) -> None:
    """Write new version to manifest.json."""
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    manifest['version'] = new_version

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)
        f.write('\n')  # Add trailing newline


def increment_alpha(version_string: str) -> Optional[str]:
    """
    Increment the alpha build number.

    Args:
        version_string: Current version (e.g., "0.1.0-alpha.1")

    Returns:
        New version string or None if parsing failed
    """
    components = parse_version(version_string)
    if not components:
        return None

    major, minor, patch, alpha = components
    new_alpha = alpha + 1

    return format_version(major, minor, patch, new_alpha)


def validate_version(version_string: str) -> bool:
    """Validate version string format."""
    return parse_version(version_string) is not None


def main():
    """Main entry point."""
    try:
        manifest_path = find_manifest()
        current_version = read_current_version(manifest_path)

        # Handle command line arguments
        if len(sys.argv) > 1:
            arg = sys.argv[1]

            if arg == '--show':
                print(current_version)
                return 0
            elif arg == '--help' or arg == '-h':
                print(__doc__)
                return 0
            else:
                # Custom version specified
                new_version = arg
                if not validate_version(new_version):
                    print(f"Error: Invalid version format '{new_version}'", file=sys.stderr)
                    print("Expected format: 0.1.0-alpha.X", file=sys.stderr)
                    return 1
        else:
            # Auto-increment
            new_version = increment_alpha(current_version)
            if not new_version:
                print(f"Error: Could not parse current version '{current_version}'", file=sys.stderr)
                return 1

        # Write new version
        write_version(manifest_path, new_version)

        # Output result (for scripting)
        print(f"{current_version} → {new_version}")
        print(f"Updated {manifest_path}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
