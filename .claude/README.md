# Claude Code Project Configuration

This directory contains Claude Code project configuration files that help Claude understand and work with the TCP to Event Converter Home Assistant integration.

## Directory Structure

```
.claude/
├── README.md           # This file
├── system_prompt.md    # Project context and guidelines
└── commands/           # Custom slash commands
    ├── analyze.md      # Code analysis command
    ├── review.md       # Pre-commit review command
    └── test.md         # Integration testing command
```

## Files Overview

### system_prompt.md

The main context file that provides Claude with:
- Complete project overview and architecture
- File-by-file descriptions
- Development guidelines specific to Home Assistant integrations
- Coding standards (async/await, error handling, logging)
- Security considerations
- Common patterns and best practices
- Testing approaches
- Troubleshooting guides

**Usage**: Automatically loaded when Claude starts working on this project.

### commands/analyze.md

A comprehensive code analysis command that reviews:
- Code quality and maintainability
- Home Assistant integration best practices
- Security vulnerabilities
- Error handling completeness
- Performance concerns
- Documentation completeness
- Type safety
- Async/await correctness

**Usage**: Run `/analyze` to perform a full codebase analysis.

### commands/test.md

A testing guide and helper that provides:
- Multiple testing methods (netcat, Python, telnet)
- Test scripts and examples
- Event monitoring instructions
- Debug logging setup
- Common issues and solutions
- Test scenario checklists

**Usage**: Run `/test` to get testing assistance.

### commands/review.md

A pre-commit review command that checks:
- All uncommitted changes
- Code quality issues
- Home Assistant standards compliance
- Security implications
- Documentation updates
- Version bumping
- Breaking changes

**Usage**: Run `/review` before committing changes.

## Using Custom Commands

To use a custom command:

```
/analyze    - Perform comprehensive code analysis
/test       - Get testing guidance and tools
/review     - Review changes before committing
```

## Customization

Feel free to:
- Add new commands in the `commands/` directory
- Update `system_prompt.md` as the project evolves
- Create project-specific workflows
- Add environment-specific configurations

## Version Control

The `.claude/` directory can be committed to git to share project context with:
- Team members using Claude Code
- Future AI-assisted development sessions
- Documentation of project structure and patterns

## Best Practices

1. **Keep system_prompt.md updated** as architecture changes
2. **Add commands for repetitive tasks** your team performs
3. **Document project-specific patterns** in system_prompt.md
4. **Update commands** as workflows evolve
5. **Share improvements** with the team

## Need Help?

- Check the system_prompt.md for project context
- Run `/analyze` to understand current codebase state
- Run `/test` for testing assistance
- Run `/review` before making commits

---

Generated for the TCP to Event Converter Home Assistant Custom Integration
