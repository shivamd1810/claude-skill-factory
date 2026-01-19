# Anthropic SKILL.md Specification

Complete specification for Claude Code skills based on Anthropic's official documentation.

## Overview

Skills are markdown files that provide Claude Code with specialized knowledge and instructions for specific tasks. They can auto-trigger based on context or be invoked via slash commands.

## File Format

Skills use markdown with YAML frontmatter:

```markdown
---
name: skill-name
description: |
  Multi-line description with trigger phrases.
  Use when: specific scenario
  Triggers for: "phrase1", "phrase2"
context: fork  # optional
---

# Skill Title

Skill content in markdown...
```

## Frontmatter Fields

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier, lowercase with dashes |
| `description` | string | Multi-line description with trigger scenarios |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `context` | enum | `fork` or `append` - conversation context handling |
| `version` | string | Semantic version (e.g., "1.0.0") |
| `author` | string | Skill author name |
| `license` | string | License identifier (e.g., "MIT") |
| `hooks` | array | PreToolUse/PostToolUse hooks |

### Context Values

| Value | Behavior |
|-------|----------|
| `fork` | Creates isolated conversation context |
| `append` | Adds instructions to current context |
| (default) | Instructions appended to context |

## Hooks Configuration

```yaml
hooks:
  - type: PreToolUse
    tool: Edit
    script: scripts/pre-edit.sh
  - type: PostToolUse
    tool: Write
    script: scripts/post-write.sh
```

### Hook Types

| Type | Trigger | Purpose |
|------|---------|---------|
| `PreToolUse` | Before tool execution | Validate, modify, or block |
| `PostToolUse` | After tool execution | Process output, notify, log |

### Hook Scripts

Scripts receive JSON via stdin:
```json
{
  "tool": "Edit",
  "parameters": { ... },
  "result": { ... }  // PostToolUse only
}
```

Exit codes:
- `0` - Success, continue
- `1` - Warning, continue
- `2` - Block operation (PreToolUse only)

## Content Guidelines

### Structure

```markdown
# Main Title

Brief introduction.

## Section 1

Content...

### Subsection

More detail...

## Examples

### Example: Title

**Context:** When to use

**Input:**
```language
code
```

**Output:**
```
expected result
```
```

### Writing Style

1. **Imperative form** - "Run tests" not "You should run tests"
2. **Specific examples** - Realistic code, not foo/bar placeholders
3. **Progressive disclosure** - Keep main file concise
4. **Clear structure** - Logical header hierarchy

### Length Guidelines

| File | Recommended | Maximum |
|------|-------------|---------|
| SKILL.md | 200-300 lines | 500 lines |
| references/* | No limit | - |

## Directory Structure

### Minimal Skill

```
my-skill/
└── SKILL.md
```

### Standard Skill

```
my-skill/
├── SKILL.md
└── references/
    └── detailed-guide.md
```

### Full Skill

```
my-skill/
├── SKILL.md
├── references/
│   ├── guide.md
│   └── examples.md
├── scripts/
│   ├── helper.py
│   └── validate.sh
└── manifest.json
```

## Installation Locations

### Personal Skills

```
~/.claude/skills/
├── my-skill/
│   └── SKILL.md
└── another-skill/
    └── SKILL.md
```

### Project Skills

```
project/
├── .claude/
│   └── skills/
│       └── project-skill/
│           └── SKILL.md
└── src/
```

### Plugin Skills

```
~/.claude/plugins/
└── my-plugin/
    ├── .claude-plugin/
    │   └── plugin.json
    └── SKILL.md
```

## Auto-Triggering

Skills auto-trigger based on description content:

### Good Triggers

```yaml
description: |
  Analyze code for security vulnerabilities.
  Use when: reviewing code for OWASP issues, security audit,
  checking for injection vulnerabilities.
  Triggers for: "security review", "check for vulnerabilities",
  "OWASP audit", "find security issues"
```

### Trigger Best Practices

1. Include 3-5 natural phrases
2. Be specific to avoid false positives
3. Include variations (singular/plural, synonyms)
4. Add "Use when" scenarios

## Commands (Slash Commands)

Skills can define invokable commands:

### Command File

`commands/my-command.md`:
```yaml
---
name: my-command
description: Short description shown in help
args: <required> [optional]
---

# Command Instructions

When /my-command is invoked...
```

### Command Registration

In `plugin.json`:
```json
{
  "commands": [
    {
      "name": "my-command",
      "path": "commands/my-command.md",
      "description": "What this command does"
    }
  ]
}
```

## Agents (Forked Context)

For conversational assistants:

```yaml
---
name: my-agent
description: Interactive assistant for...
context: fork
---

# Agent Name

You are [persona] who helps with [task].

## Your Role

[Detailed instructions]

## Conversation Flow

[How to interact]
```

## Best Practices Summary

1. **Single purpose** - One skill, one task
2. **Clear triggers** - Specific, natural phrases
3. **Progressive disclosure** - Main file concise
4. **Realistic examples** - No placeholders
5. **Imperative form** - Direct instructions
6. **Proper structure** - Logical organization
7. **Cross-references** - Link to references/

## References

- [Official Anthropic Skills Guide](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
