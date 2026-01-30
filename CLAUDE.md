# CLAUDE.md - AI Assistant Guide

This file provides context and guidance for AI assistants working with this codebase.

## Project Overview

**Repository:** first-test-project
**Owner:** ko-minseok
**Status:** Starter/Template project (minimal setup phase)

This is a personal test project in its initial setup phase. The repository currently contains only a README template and is ready for development content to be added.

## Current Project Structure

```
first-test-project/
├── .git/              # Git repository metadata
├── CLAUDE.md          # This file - AI assistant guidelines
└── README.md          # Project documentation template (Korean/English)
```

## Technology Stack

**Not yet established.** The README template suggests potential support for:
- Python (mentions `__pycache__/`, `*.pyc`, `venv/`)
- Node.js (mentions `node_modules/`)

When the project evolves, update this section with the actual stack.

## Development Setup

### Prerequisites
No dependencies or build tools are currently configured.

### Getting Started
```bash
git clone <repository-url>
cd first-test-project
```

## Git Workflow

### Branch Naming
- Feature branches: `claude/<description>-<session-id>`
- Main development happens on feature branches
- Push changes with: `git push -u origin <branch-name>`

### Commit Messages
- Use clear, descriptive commit messages
- Prefix with action type when applicable: `Add`, `Update`, `Fix`, `Remove`

## AI Assistant Guidelines

### When Working on This Project

1. **Check current state first**: This is a minimal project. Always verify what files exist before making assumptions.

2. **Suggested initial setup tasks** (if asked to set up the project):
   - Create `.gitignore` file with appropriate ignores
   - Initialize package management (`package.json` or `requirements.txt`)
   - Set up project structure (`src/`, `tests/`, etc.)
   - Configure build/development tooling
   - Add testing framework

3. **Documentation language**: The README contains Korean (한국어) documentation. Maintain bilingual support if adding documentation.

4. **Keep it simple**: This is a test project. Avoid over-engineering.

### Code Conventions (To Be Established)

When code is added to this project, follow these general best practices:
- Use consistent formatting (configure Prettier/ESLint for JS/TS, Black for Python)
- Write clear, self-documenting code
- Add tests for new functionality
- Keep functions focused and single-purpose

### File Organization (Recommended Structure)

When expanding the project, consider this structure:
```
first-test-project/
├── src/               # Source code
│   ├── components/    # UI components (if applicable)
│   ├── utils/         # Utility functions
│   └── index.ts       # Entry point
├── tests/             # Test files
├── docs/              # Additional documentation
├── .gitignore         # Git ignore rules
├── package.json       # Dependencies (for Node.js)
├── tsconfig.json      # TypeScript config (if using TS)
├── CLAUDE.md          # This file
└── README.md          # Project documentation
```

## Common Tasks

### Adding New Features
1. Create a feature branch
2. Implement the feature with tests
3. Update documentation if needed
4. Commit with clear messages
5. Push to remote

### Debugging
- Check existing code patterns before adding new solutions
- Review README.md for project-specific guidance

## Notes for AI Assistants

- **This is a starter project**: Most infrastructure is not yet set up
- **Language context**: Project uses Korean in documentation; be prepared to work bilingually
- **Be minimal**: Only add what's necessary for the current task
- **Update this file**: When significant project changes occur, update CLAUDE.md accordingly

## Last Updated

2026-01-30 - Initial CLAUDE.md creation documenting starter project state
