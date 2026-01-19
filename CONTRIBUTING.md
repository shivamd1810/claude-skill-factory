# Contributing to Claude Skill Factory

Thank you for your interest in contributing! This document provides guidelines for contributing to the Claude Skill Factory project.

## Ways to Contribute

### 1. Submit New Templates

Create templates for new use cases:

```
templates/
└── your-template/
    └── SKILL.template.md
```

**Requirements:**
- Clear placeholder syntax (`{{PLACEHOLDER_NAME}}`)
- Comprehensive comments explaining the template
- Example values in comments
- Follow existing template patterns

### 2. Improve Validation Rules

Enhance the validation framework:

- Add new checks to `scripts/validate-skill.py`
- Update `references/validation-rules.md`
- Ensure backward compatibility

### 3. Submit Example Skills

Add production-quality example skills:

```
examples/
└── your-example-skill/
    ├── SKILL.md
    └── references/
```

**Requirements:**
- Score >= 80 using `/skill-score`
- Pass all validation checks
- Include realistic examples

### 4. Improve Documentation

- Fix typos and clarify explanations
- Add more examples
- Improve reference documentation
- Translate to other languages

### 5. Report Issues

Open issues for:
- Bugs in validation/scoring
- Template improvements
- Feature requests
- Documentation gaps

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shivamd1810/claude-skill-factory
   cd claude-skill-factory
   ```

2. **Test the scripts:**
   ```bash
   python3 scripts/validate-skill.py templates/simple
   python3 scripts/score-skill.py templates/simple
   ```

3. **Install as plugin (for testing):**
   ```bash
   ln -s $(pwd) ~/.claude/plugins/skill-factory
   ```

## Pull Request Process

### Before Submitting

1. **Run validation on any new/modified skills:**
   ```bash
   python3 scripts/validate-skill.py <path>
   ```

2. **Check quality score:**
   ```bash
   python3 scripts/score-skill.py <path>
   ```

3. **Test commands work correctly**

### PR Requirements

1. **Clear description** of what the PR changes
2. **Link related issues** if applicable
3. **Update documentation** if needed
4. **Pass all checks** (validation, scoring)

### Commit Messages

Follow conventional commits:

```
feat: add new workflow template
fix: correct validation for empty files
docs: improve trigger phrase documentation
test: add validation test cases
```

## Code Style

### Python Scripts

- Use Python 3.8+ features
- Include docstrings for classes and functions
- Follow PEP 8 style guidelines
- Add type hints where helpful

### Markdown Files

- Use ATX-style headers (`#`, `##`)
- Include language tags on code blocks
- Use tables for structured data
- Keep lines under 100 characters where practical

### YAML Frontmatter

- Use lowercase field names
- Quote strings with special characters
- Use `|` for multi-line strings

## Template Guidelines

When creating templates:

### Placeholder Syntax

```markdown
{{PLACEHOLDER_NAME}}
```

- Use SCREAMING_SNAKE_CASE
- Be descriptive: `{{STEP_1_VERIFICATION_COMMAND}}`
- Group related placeholders

### Template Comments

Include a comment block at the end:

```markdown
<!--
TEMPLATE: template-name
USE FOR: Specific use case description
CHARACTERISTICS:
- Key feature 1
- Key feature 2

DIRECTORY STRUCTURE:
skill-name/
├── SKILL.md
└── references/

PLACEHOLDER GUIDE:
- {{SKILL_NAME}}: lowercase-with-dashes
- {{TRIGGER_N}}: Natural phrases users say
-->
```

## Validation Rule Guidelines

When adding validation rules:

### Rule Structure

```python
def validate_new_check(self) -> ValidationResult:
    """Check N: Description of what this validates."""
    issues = []

    # Perform checks
    if condition_fails:
        issues.append("Specific issue description")

    if issues:
        return ValidationResult("CheckName", False, "Summary", issues)
    return ValidationResult("CheckName", True, "Success message")
```

### Documentation

Update `references/validation-rules.md` with:
- What the rule checks
- Pass/fail criteria
- Examples of good/bad
- How to fix issues

## Scoring Guidelines

When modifying the scoring rubric:

### Point Allocation

- Ensure total remains 100 points
- Weight categories by importance
- Provide granular scoring within categories

### Documentation

Update `references/quality-rubric.md` with:
- Point breakdown
- Criteria for each score level
- Examples at different score levels

## Questions?

- Open a discussion on GitHub
- Check existing issues and PRs
- Review the documentation

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow GitHub's community guidelines

Thank you for contributing!
