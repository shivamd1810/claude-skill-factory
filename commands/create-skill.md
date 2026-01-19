---
name: create-skill
description: Launch interactive wizard to create a new Claude Code skill
---

# Create Skill Command

Launch an interactive wizard that guides you through creating a high-quality Claude Code skill.

## Usage

```
/create-skill
```

No arguments required - the wizard will ask for all needed information.

## What Happens

When you invoke this command:

1. **The skill-wizard agent activates** with a forked context
2. **You'll be asked questions** about your skill:
   - What task should it accomplish?
   - What phrases would trigger it?
   - What's the expected output?
   - Does it need scripts or references?

3. **A template is selected** based on your needs:
   | Your Needs | Template |
   |------------|----------|
   | Simple guidelines | `simple` |
   | Guidelines + docs | `standard` |
   | Multi-step process | `workflow` |
   | CLI/API wrapper | `tool-integration` |
   | Domain expertise | `domain-expert` |
   | Assistant persona | `forked-agent` |
   | Auto-trigger hooks | `hook-enabled` |
   | Cross-platform | `cross-platform` |

4. **Files are generated** with your content:
   - SKILL.md (main skill file)
   - references/ (if needed)
   - scripts/ (if needed)

5. **Validation runs automatically:**
   - 7-point best practices check
   - Quality score (0-100)
   - Recommendations for improvement

6. **You choose the output location:**
   - `~/.claude/skills/[name]` for personal use
   - `.claude/skills/[name]` for project-specific

## Example Session

```
> /create-skill

Wizard: I'll help you create a Claude Code skill. Let's start with the basics.

What task should this skill help with? Describe it in a sentence or two.

You: I want a skill that helps review pull requests for security issues.

Wizard: Great! A security-focused PR review skill. Let me ask a few more questions:

1. What phrases would trigger this skill?
   - "review PR for security"
   - "security audit this PR"
   - What else?

You: Also "check for vulnerabilities" and "OWASP review"

Wizard: Perfect. What should the output include?
   - List of potential issues?
   - Severity ratings?
   - Remediation suggestions?

You: All of those, with code snippets showing the problems.

Wizard: This sounds like a domain-expert skill. I'll create:

security-pr-review/
├── SKILL.md              # Main review guidelines
└── references/
    ├── owasp-top-10.md   # OWASP vulnerability details
    └── remediation.md    # Fix patterns

Where should I create it?
1. ~/.claude/skills/security-pr-review (personal)
2. .claude/skills/security-pr-review (this project)

You: Personal please

Wizard: Creating skill...

[Files created]

Running validation...
✓ Structure: PASS
✓ Frontmatter: PASS
✓ Description: PASS
✓ Content: PASS
✓ Progressive Disclosure: PASS
✓ Resources: PASS
✓ Cross-Platform: PASS (with recommendations)

Score: 85/100 (Grade: B)

Your skill is ready! Test it by asking Claude to "review this PR for security issues"

Would you like me to:
- Add more examples?
- Improve the score to 90+?
- Package it for sharing?
```

## Tips for Good Skills

When answering the wizard's questions:

### For Triggers
- Use phrases you'd naturally say
- Be specific: "analyze CSV" not "help with files"
- Include variations: "review PR", "check pull request"

### For Content
- Think about edge cases
- Consider error scenarios
- Include realistic examples

### For Structure
- Start simple, add complexity if needed
- Keep main file focused
- Move details to references

## After Creation

Once your skill is created:

1. **Test it** - Try your trigger phrases
2. **Iterate** - Use `/skill-score` to improve
3. **Share** - Use `/package-skill` for distribution

## Related Commands

- `/validate-skill <path>` - Check skill against best practices
- `/skill-score <path>` - Get quality score
- `/package-skill <path>` - Package for distribution
