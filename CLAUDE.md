# CLAUDE.md - AI Assistant Guide for Micksiney

This file provides guidance for AI assistants working with the Micksiney codebase.

## Repository Overview

**Repository:** Econ-git871/Micksiney
**Status:** New repository - initial setup phase

This repository is currently being initialized. As the project develops, this document will be updated with specific details about the codebase structure, patterns, and conventions.

## Project Structure

```
Micksiney/
├── CLAUDE.md          # This file - AI assistant guidance
└── (additional structure to be added)
```

*Note: Update this section as the project structure evolves.*

## Development Workflow

### Git Workflow

1. **Branch Naming Convention**
   - Feature branches: `feature/<description>`
   - Bug fixes: `fix/<description>`
   - AI-assisted branches: `claude/<session-identifier>`

2. **Commit Messages**
   - Use clear, descriptive commit messages
   - Start with a verb in imperative mood (Add, Fix, Update, Remove, Refactor)
   - Keep the first line under 72 characters
   - Add detailed description in the body if needed

3. **Pull Requests**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure all tests pass before merging

### Code Review Guidelines

- Review for correctness, readability, and maintainability
- Check for potential security vulnerabilities
- Ensure code follows project conventions
- Verify adequate test coverage for new features

## Code Conventions

### General Guidelines

1. **Code Style**
   - Follow consistent indentation (define standard as project develops)
   - Use meaningful variable and function names
   - Keep functions focused and single-purpose
   - Write self-documenting code where possible

2. **Documentation**
   - Add comments for complex logic
   - Document public APIs and interfaces
   - Keep documentation up to date with code changes

3. **Error Handling**
   - Handle errors gracefully
   - Provide meaningful error messages
   - Log errors appropriately for debugging

### Security Practices

- Never commit secrets, API keys, or credentials
- Validate all user inputs
- Use parameterized queries for database operations
- Follow OWASP security guidelines

## Testing

### Testing Strategy

- Write tests for new features
- Maintain existing test coverage
- Run tests before committing changes

### Running Tests

*Note: Add specific test commands as testing infrastructure is set up.*

```bash
# Example test commands (update as needed)
# npm test
# pytest
# go test ./...
```

## Build and Deployment

*Note: Document build and deployment processes as they are established.*

### Local Development

```bash
# Clone the repository
git clone <repository-url>

# Navigate to project directory
cd Micksiney

# Additional setup steps to be added
```

## AI Assistant Guidelines

### When Working on This Codebase

1. **Before Making Changes**
   - Read and understand existing code before modifying
   - Check for existing patterns and follow them
   - Review related tests and documentation

2. **Making Changes**
   - Make minimal, focused changes
   - Avoid over-engineering solutions
   - Don't add unnecessary features or refactoring
   - Keep changes within the scope of the request

3. **Code Quality**
   - Follow existing code style and patterns
   - Ensure changes don't introduce security vulnerabilities
   - Write clear, maintainable code

4. **Communication**
   - Explain significant decisions or trade-offs
   - Ask for clarification when requirements are unclear
   - Document any assumptions made

### Important Notes for AI Assistants

- **Never** commit sensitive information (keys, passwords, tokens)
- **Always** test changes when possible
- **Prefer** editing existing files over creating new ones
- **Avoid** making changes to code you haven't read
- **Keep** solutions simple and focused on the task at hand

## Configuration Files

*Note: Document key configuration files as they are added to the project.*

| File | Purpose |
|------|---------|
| `CLAUDE.md` | AI assistant guidance |
| `.gitignore` | Git ignore rules (to be added) |

## Dependencies

*Note: Document project dependencies as they are established.*

## Troubleshooting

### Common Issues

*Add common issues and solutions as they are encountered.*

## Contributing

### Getting Started

1. Fork the repository (if applicable)
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

### Code of Conduct

- Be respectful and constructive
- Focus on the code, not the person
- Welcome newcomers and help them contribute

---

## Changelog

| Date | Description |
|------|-------------|
| 2025-12-02 | Initial CLAUDE.md created |

---

*This document should be updated as the project evolves. When adding new features, patterns, or conventions, please update the relevant sections.*
