# Claude Skill Factory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.com/claude-code)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-compatible-green)](https://agentskills.io)

> Create, validate, and distribute high-quality Claude Code skills following Anthropic's best practices and the cross-platform agentskills.io standard.

## Features

- **Interactive Skill Wizard** - Guided creation through conversational Q&A
- **8 Production Templates** - From simple guidelines to complex workflows
- **7-Point Validation** - Check skills against Anthropic's best practices
- **Quality Scoring** - Rate skills 0-100 with detailed breakdown
- **Cross-Platform Ready** - agentskills.io compatible for portability
- **One-Click Packaging** - Create distribution-ready ZIPs

## Quick Start

### Installation

```bash
# Clone to your plugins directory
git clone https://github.com/shivamd1810/claude-skill-factory ~/.claude/plugins/skill-factory
```

### Create Your First Skill

```
> /create-skill

Wizard: What task should this skill help with?

You: I want a skill that reviews Python code for best practices.

Wizard: Great! I'll create a code-review skill with:
- Trigger phrases for auto-activation
- Python best practices checklist
- Example reviews with feedback

Where should I create it?
```

## Commands

| Command | Description |
|---------|-------------|
| `/create-skill` | Launch interactive creation wizard |
| `/validate-skill <path>` | Run 7-point best practices validation |
| `/skill-score <path>` | Get quality score (0-100) with breakdown |
| `/package-skill <path>` | Create distribution-ready ZIP |

## Templates

Choose the right template for your skill:

| Template | Use Case | Example |
|----------|----------|---------|
| **simple** | Knowledge-only, no scripts | Code style guides |
| **standard** | Guidelines with references | API integration guides |
| **workflow** | Multi-step processes | Deployment procedures |
| **tool-integration** | Wrapping CLI tools/APIs | Git workflows |
| **domain-expert** | Deep domain knowledge | Security auditing |
| **forked-agent** | Conversational assistants | Interactive wizards |
| **hook-enabled** | Auto-trigger on tool use | Auto-formatting |
| **cross-platform** | Work across AI tools | Portable skills |

## Quality Standards

### 7-Point Validation

1. **Structure** - Correct files and directories
2. **Frontmatter** - Valid name and description
3. **Description** - Trigger phrases for auto-activation
4. **Content** - Clear, imperative instructions
5. **Progressive Disclosure** - Main file concise
6. **Resources** - Referenced files exist
7. **Cross-Platform** - agentskills.io compatibility

### Quality Scoring (100 points)

| Category | Points |
|----------|--------|
| Structure | 15 |
| Description | 25 |
| Content | 25 |
| Progressive Disclosure | 15 |
| Examples | 10 |
| Cross-Platform | 10 |

**Grade Scale:**
- **A (90+)** - Production ready
- **B (80-89)** - Meets standards
- **C (70-79)** - Needs improvement
- **D/F (<70)** - Significant work needed

## Directory Structure

```
claude-skill-factory/
├── SKILL.md                    # Main skill (auto-triggers)
├── commands/                   # Slash commands
│   ├── create-skill.md        # /create-skill
│   ├── validate-skill.md      # /validate-skill
│   ├── skill-score.md         # /skill-score
│   └── package-skill.md       # /package-skill
├── agents/                     # Forked context agents
│   ├── skill-wizard.md        # Creation wizard
│   └── skill-reviewer.md      # Quality reviewer
├── templates/                  # 8 skill templates
│   ├── simple/
│   ├── standard/
│   ├── workflow/
│   ├── tool-integration/
│   ├── domain-expert/
│   ├── forked-agent/
│   ├── hook-enabled/
│   └── cross-platform/
├── scripts/                    # Python utilities
│   ├── validate-skill.py
│   ├── score-skill.py
│   └── package-skill.py
└── references/                 # Documentation
    ├── anthropic-spec.md
    ├── validation-rules.md
    └── quality-rubric.md
```

## Skill Best Practices

### Description with Triggers

```yaml
description: |
  Analyze code for security vulnerabilities.
  Use when: reviewing code for OWASP issues, security audit.
  Triggers for: "security review", "check vulnerabilities"
```

### Imperative Form

```markdown
# Good
Run tests before committing.
Check for type errors.

# Avoid
You should run tests before committing.
You can check for type errors.
```

### Progressive Disclosure

```
my-skill/
├── SKILL.md              # Core instructions (<500 lines)
└── references/
    └── detailed-guide.md # Extended documentation
```

## Cross-Platform Support

Skills can work across multiple AI coding assistants:

| Platform | Support |
|----------|---------|
| Claude Code | Native |
| Gemini CLI | Compatible |
| Cursor | Compatible |
| Aider | Partial |
| Continue | Compatible |

Add agentskills.io fields for portability:

```yaml
---
name: my-skill
version: "1.0.0"
platforms:
  - claude-code
  - gemini-cli
  - cursor
tags:
  - python
  - code-review
---
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- Add new templates
- Improve validation rules
- Submit example skills
- Report issues
- Improve documentation

## Resources

- [Anthropic Skills Guide](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Claude Code Documentation](https://code.claude.com/docs/en/skills)
- [agentskills.io Specification](https://agentskills.io/specification)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Keywords:** Claude Code, skills, plugins, AI agents, agentskills.io, prompt engineering, LLM tools, Gemini CLI, Cursor, automation
