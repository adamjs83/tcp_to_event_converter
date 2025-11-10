# Versioning Strategy

This project follows [Semantic Versioning 2.0.0](https://semver.org/) with alpha/beta release markers.

## Version Format

```
MAJOR.MINOR.PATCH-PRERELEASE.BUILD
```

### Examples:
- `0.1.0-alpha.1` - First alpha of version 0.1.0
- `0.1.0-alpha.2` - Second alpha of version 0.1.0
- `0.2.0-beta.1` - First beta of version 0.2.0
- `1.0.0` - First stable release

## Current Status: ALPHA

**Version:** `0.1.0-alpha.1`

The project is currently in **ALPHA** stage, which means:

- The API may change without notice
- Breaking changes may occur between alpha releases
- Features may be incomplete or experimental
- Bugs and issues are expected
- NOT recommended for production use
- Limited testing has been performed

## Version History

### Alpha Phase (0.x.x-alpha.x)

The 0.x.x version indicates the project is in pre-release development:

- **Major version 0** = Not yet production-ready
- **Minor version** increments with new features or significant changes
- **Patch version** increments with bug fixes and minor improvements
- **Alpha build number** increments with each alpha release

### Future Beta Phase (0.x.x-beta.x)

Beta releases will be created when:
- Core functionality is feature-complete
- Major bugs are resolved
- API is stabilizing
- Ready for broader testing

Beta releases indicate:
- Feature-complete but still testing
- API changes are rare and documented
- More stable than alpha but not production-ready
- Suitable for testing environments

### Stable Release (1.0.0)

Version 1.0.0 will be released when:
- All planned core features are implemented and tested
- No known critical bugs
- API is stable with commitment to backward compatibility
- Documentation is complete
- Extensive testing completed
- Production-ready

## Release Checklist

### For Each Alpha Release

- [ ] Update version in `manifest.json`
- [ ] Update version in README badges
- [ ] Update CHANGELOG with release notes
- [ ] Tag release in git: `git tag v0.x.x-alpha.x`
- [ ] Push tag: `git push origin v0.x.x-alpha.x`
- [ ] Create GitHub release with alpha warning

### For Beta Release

- [ ] Complete alpha testing phase
- [ ] Resolve all critical issues
- [ ] Update to beta version format
- [ ] Update README to reflect beta status
- [ ] Comprehensive testing completed
- [ ] Tag and release as beta

### For Stable Release

- [ ] Complete beta testing phase
- [ ] No known critical issues
- [ ] All features tested and documented
- [ ] Update to 1.0.0 version
- [ ] Remove alpha/beta warnings
- [ ] Create comprehensive release notes
- [ ] Tag and release as stable

## Semantic Versioning Rules

Once stable (1.0.0+):

### MAJOR version (1.0.0 -> 2.0.0)
Incremented when making incompatible API changes:
- Breaking changes to configuration format
- Removal of features or options
- Changes that require user migration

### MINOR version (1.0.0 -> 1.1.0)
Incremented when adding functionality in a backward-compatible manner:
- New features
- New configuration options (with defaults)
- Deprecations (but not removals)

### PATCH version (1.0.0 -> 1.0.1)
Incremented when making backward-compatible bug fixes:
- Bug fixes
- Performance improvements
- Documentation updates
- Security patches

## Backward Compatibility Promise

Starting from version 1.0.0:
- PATCH releases: 100% backward compatible
- MINOR releases: Backward compatible with possible deprecations
- MAJOR releases: May include breaking changes with migration guide

During alpha/beta (0.x.x):
- No backward compatibility guarantees
- Breaking changes may occur at any time
- Users should expect to update configurations

## Version Update Process

1. Decide version number based on changes
2. Update `custom_components/tcp_to_event_converter/manifest.json`
3. Update README.md badges and changelog
4. Commit changes: `git commit -m "Bump version to X.X.X"`
5. Create git tag: `git tag vX.X.X`
6. Push commits and tags: `git push && git push --tags`
7. Create GitHub release with release notes

## Current Roadmap

### Path to Beta (0.x.0-beta.1)
- Comprehensive testing with various devices
- Complete documentation
- Security audit
- Performance optimization
- Edge case handling

### Path to Stable (1.0.0)
- Extended beta testing period
- Community feedback integration
- Production environment testing
- Final API stabilization
- Complete test coverage

## Questions?

If you have questions about versioning or release status, please:
- Check the [GitHub Releases](https://github.com/adamjs83/tcp_to_event_converter/releases) page
- Review the [CHANGELOG](README.md#changelog)
- Open an [issue](https://github.com/adamjs83/tcp_to_event_converter/issues)
