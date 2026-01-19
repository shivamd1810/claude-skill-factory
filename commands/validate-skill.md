---
name: validate-skill
description: Run 7-point validation against Claude Code skill best practices
args: <path>
---

# Validate Skill Command

Validate a Claude Code skill against Anthropic's best practices using a 7-point validation framework.

## Usage

```
/validate-skill <path-to-skill>
```

**Arguments:**
- `<path>` - Path to skill directory or SKILL.md file

## Validation Process

When this command is invoked:

1. **Locate the skill** at the provided path
2. **Run the validation script**:
   ```bash
   python3 scripts/validate-skill.py <path>
   ```
3. **Display results** showing pass/fail for each check
4. **Provide recommendations** for any failed checks

## 7-Point Validation Criteria

| # | Check | What It Validates |
|---|-------|-------------------|
| 1 | Structure | SKILL.md exists, directories properly organized |
| 2 | Frontmatter | Required `name` and `description` fields present and valid |
| 3 | Description | Contains trigger phrases, specific scenarios |
| 4 | Content | Uses imperative form, has examples, proper length |
| 5 | Progressive Disclosure | Main file <500 lines, details in references/ |
| 6 | Resources | Referenced files exist, scripts are executable |
| 7 | Cross-Platform | agentskills.io compatibility (optional) |

## Example Output

```
=== Skill Validation Report ===

Skill: my-skill
Path: /path/to/my-skill

[PASS] Structure: Directory structure is valid

[PASS] Frontmatter: Frontmatter is valid

[FAIL] Description: Description quality issues
       - No trigger phrases found in description
       - Add phrases like 'Triggers for: "phrase1", "phrase2"'

[PASS] Content: Content is well-structured

[PASS] Progressive Disclosure: Good progressive disclosure

[PASS] Resources: All referenced resources exist

[PASS] Cross-Platform: Optional cross-platform improvements
       - Consider adding agentskills.io fields for cross-platform compatibility

=== Summary ===
6/7 checks passed
```

## Actions After Validation

Based on results:

| Result | Action |
|--------|--------|
| All 7 passed | Skill is ready for use or distribution |
| 5-6 passed | Address minor issues before sharing |
| 3-4 passed | Significant improvements needed |
| <3 passed | Major restructuring required |

## JSON Output

For programmatic use:

```bash
python3 scripts/validate-skill.py <path> --json
```

Returns structured JSON with all validation results.
