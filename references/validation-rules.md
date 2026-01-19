# Validation Rules Reference

Detailed documentation of the 7-point validation framework for Claude Code skills.

## Overview

The validation framework checks skills against Anthropic's best practices across seven categories:

1. Structure
2. Frontmatter
3. Description
4. Content
5. Progressive Disclosure
6. Resources
7. Cross-Platform

## Check 1: Structure

**Purpose:** Ensure correct file organization

### Required

| Check | Requirement |
|-------|-------------|
| SKILL.md | Must exist in skill root |
| Directory | Must be a valid directory |

### Conditional

| Check | When Required |
|-------|---------------|
| references/ | If referenced in SKILL.md |
| scripts/ | If referenced in SKILL.md |

### Warnings

| Issue | Message |
|-------|---------|
| Junk files | `.DS_Store`, `Thumbs.db`, `__pycache__` found |
| Empty directories | Directory exists but contains no files |

### Pass Criteria

- SKILL.md exists
- Referenced directories exist
- No structural inconsistencies

## Check 2: Frontmatter

**Purpose:** Validate required metadata fields

### Required Fields

| Field | Validation |
|-------|------------|
| `name` | Must exist, match `/^[a-z0-9-]+$/` |
| `description` | Must exist, minimum 20 characters |

### Optional Fields

| Field | Validation |
|-------|------------|
| `context` | If present, must be `fork` or `append` |
| `version` | If present, should match semver |
| `hooks` | If present, must be valid array |

### Examples

**Valid:**
```yaml
name: my-skill
description: |
  Helps with specific task.
  Triggers for: "phrase1", "phrase2"
```

**Invalid:**
```yaml
name: My Skill  # Uppercase, spaces
description: Hi  # Too short
```

### Pass Criteria

- `name` exists and follows convention
- `description` exists and has sufficient content
- Optional fields (if present) are valid

## Check 3: Description Quality

**Purpose:** Ensure effective auto-triggering

### Trigger Detection

Looks for patterns:
- `Triggers for:`
- `Activates when:`
- `Use when:`
- Quoted phrases: `"phrase1", "phrase2"`

### Specificity Check

**Generic words to avoid:**
- help, assist, support
- various, many, different
- things, stuff, general

**Specific indicators:**
- When, for, to
- Specific nouns (CSV, API, Docker)
- Action verbs (analyze, deploy, validate)

### Examples

**Good:**
```yaml
description: |
  Analyze CSV files for data quality issues.
  Use when: validating spreadsheet data, checking for duplicates,
  finding missing values in datasets.
  Triggers for: "check CSV quality", "validate data file",
  "analyze spreadsheet"
```

**Bad:**
```yaml
description: |
  Help with various data tasks.
```

### Pass Criteria

- Contains at least one trigger pattern
- Specific rather than generic
- Minimum 50 characters

## Check 4: Content Quality

**Purpose:** Validate instruction clarity and format

### Imperative Form

**Check for passive patterns:**
- "You should..."
- "You can..."
- "You will..."
- "It is recommended..."

**Preferred imperative:**
- "Run..."
- "Create..."
- "Check..."
- "Verify..."

### Examples Check

Looks for:
- `## Example` headers
- Code blocks (```)
- `e.g.` or `for instance`

### Structure Check

| Element | Minimum |
|---------|---------|
| Headers (##) | 2 |
| Code blocks | 2 |
| Lists | 1 |

### Pass Criteria

- More imperative than passive voice
- Contains examples
- Has proper header structure

## Check 5: Progressive Disclosure

**Purpose:** Ensure main file is appropriately concise

### Length Limits

| Lines | Assessment |
|-------|------------|
| < 200 | Excellent |
| 200-350 | Good |
| 350-500 | Acceptable |
| > 500 | Too long |

### References Usage

| Situation | Recommendation |
|-----------|----------------|
| Main file > 300 lines | Should use references/ |
| Main file > 500 lines | Must use references/ |
| Detailed docs inline | Move to references/ |

### Section Analysis

Checks for overly long sections (> 100 lines without break).

### Pass Criteria

- Main file under 500 lines
- Long files use references/
- No monolithic sections

## Check 6: Resources

**Purpose:** Verify referenced files exist

### File Detection

Patterns scanned:
- Backtick references: `` `references/file.md` ``
- Path mentions: `references/file.md`
- Script references: `scripts/helper.py`

### Script Validation

For files in `scripts/`:
- `.sh` files must be executable
- `.py` files should be executable

### Pass Criteria

- All referenced files exist
- Scripts are executable
- No broken links

## Check 7: Cross-Platform

**Purpose:** Check agentskills.io compatibility

### agentskills.io Fields

| Field | Purpose |
|-------|---------|
| `version` | Semver version string |
| `platforms` | Array of supported platforms |
| `inputs` | Input parameter definitions |
| `outputs` | Output definitions |
| `tags` | Discovery tags |

### manifest.json

Recommended for registry listing:
```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "platforms": ["claude-code", "gemini-cli"],
  "tags": ["tag1", "tag2"]
}
```

### Pass Criteria

- Has agentskills.io fields (recommended)
- Has manifest.json (optional)
- Platform-neutral content (preferred)

## Validation Output

### Formats

**Console:**
```
[PASS] Structure: Directory structure is valid
[FAIL] Description: Description quality issues
       - No trigger phrases found
       - Add 'Triggers for:' patterns
```

**JSON:**
```json
{
  "all_passed": false,
  "results": [
    {
      "name": "Structure",
      "passed": true,
      "message": "Directory structure is valid",
      "details": []
    }
  ]
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | One or more checks failed |

## Using Validation

### Command Line

```bash
# Basic validation
python3 scripts/validate-skill.py /path/to/skill

# JSON output
python3 scripts/validate-skill.py /path/to/skill --json
```

### In Claude Code

```
/validate-skill ~/.claude/skills/my-skill
```

## Fixing Common Issues

### "No trigger phrases"

Add to description:
```yaml
description: |
  [Your description]
  Triggers for: "phrase1", "phrase2", "phrase3"
```

### "Too much passive voice"

Before: "You should run the tests"
After: "Run the tests"

### "Main file too long"

1. Create `references/` directory
2. Move detailed sections to `references/detailed-guide.md`
3. Add reference link in main file

### "Script not executable"

```bash
chmod +x scripts/my-script.sh
```

### "Referenced file not found"

Either create the file or remove the reference.
