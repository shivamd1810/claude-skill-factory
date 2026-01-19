# Quality Scoring Rubric

Detailed methodology for scoring Claude Code skills (0-100 points).

## Overview

The quality score provides a comprehensive assessment across six categories:

| Category | Max Points |
|----------|------------|
| Structure | 15 |
| Description | 25 |
| Content | 25 |
| Progressive Disclosure | 15 |
| Examples | 10 |
| Cross-Platform | 10 |
| **Total** | **100** |

## Grade Scale

| Score | Grade | Assessment |
|-------|-------|------------|
| 90-100 | A | Excellent - Production ready |
| 80-89 | B | Good - Meets standards |
| 70-79 | C | Acceptable - Needs improvement |
| 60-69 | D | Below standard - Significant work needed |
| <60 | F | Failing - Major restructuring required |

---

## Category 1: Structure (15 points)

### SKILL.md Exists (5 points)

| Points | Criteria |
|--------|----------|
| 5 | SKILL.md exists at root |
| 0 | SKILL.md missing |

### references/ Directory (4 points)

| Points | Criteria |
|--------|----------|
| 4 | references/ exists with content |
| 2 | references/ mentioned but missing |
| 0 | No references structure |

### scripts/ Directory (4 points)

| Points | Criteria |
|--------|----------|
| 4 | scripts/ with executable files |
| 3 | scripts/ exists, some not executable |
| 1 | scripts/ mentioned but missing |
| 0 | No scripts (may not be needed) |

### Clean Directory (2 points)

| Points | Criteria |
|--------|----------|
| 2 | No junk files (.DS_Store, __pycache__) |
| 0 | Contains unwanted files |

---

## Category 2: Description (25 points)

### Name Field (3 points)

| Points | Criteria |
|--------|----------|
| 3 | Valid name (lowercase-with-dashes) |
| 1 | Name exists but format incorrect |
| 0 | Missing name field |

### Description Length (5 points)

| Points | Criteria |
|--------|----------|
| 5 | 100+ characters (comprehensive) |
| 3 | 50-99 characters (adequate) |
| 1 | 20-49 characters (minimal) |
| 0 | <20 characters (too short) |

### Trigger Phrases (8 points)

**Detection patterns:**
- `Triggers for:`
- `Activates when:`
- `Use when:`
- Multiple quoted phrases

| Points | Criteria |
|--------|----------|
| 8 | Multiple trigger patterns |
| 4 | One trigger pattern |
| 0 | No trigger phrases |

### Specificity (5 points)

**Specific indicators:** when, for, to, that, which
**Generic words:** help, assist, support, various, many, general

| Points | Criteria |
|--------|----------|
| 5 | Specific (indicators > generic) |
| 3 | Moderately specific |
| 1 | Too generic |

### Context Field (4 points)

| Points | Criteria |
|--------|----------|
| 4 | Conversational skill with context:fork |
| 4 | Non-conversational (context not needed) |
| 1 | Conversational but missing context |

---

## Category 3: Content (25 points)

### Headers/Structure (6 points)

**Scoring:**
- One H1 + 3+ H2s = optimal
- 4+ headers total = good
- 2-3 headers = basic

| Points | Criteria |
|--------|----------|
| 6 | Proper header hierarchy (1 H1, 3+ H2) |
| 4 | Good header structure (4+ headers) |
| 2 | Basic structure (2-3 headers) |
| 0 | Poor structure (<2 headers) |

### Code Blocks (6 points)

| Points | Criteria |
|--------|----------|
| 6 | 4+ code blocks with language tags |
| 4 | 2-3 code blocks |
| 2 | 1 code block |
| 0 | No code blocks |

### Imperative Form (5 points)

**Passive patterns:** you should, you can, you will, you may, you need to
**Imperative patterns:** run, create, add, use, check, verify, ensure

Calculate ratio: imperative / (passive + 1)

| Points | Criteria |
|--------|----------|
| 5 | Ratio >= 3 (strong imperative) |
| 3 | Ratio >= 1.5 (good imperative) |
| 1 | Ratio >= 0.5 (too passive) |
| 0 | Ratio < 0.5 (mostly passive) |

### Tables (4 points)

Count markdown table rows (`|...|`)

| Points | Criteria |
|--------|----------|
| 4 | 6+ table rows |
| 2 | 2-5 table rows |
| 0 | No tables |

### Lists (4 points)

Count bullet (`- `) and numbered (`1. `) items

| Points | Criteria |
|--------|----------|
| 4 | 8+ list items |
| 2 | 4-7 list items |
| 0 | <4 list items |

---

## Category 4: Progressive Disclosure (15 points)

### Main File Length (8 points)

| Points | Criteria |
|--------|----------|
| 8 | <200 lines (concise) |
| 6 | 200-350 lines (good) |
| 4 | 350-500 lines (acceptable) |
| 2 | 500-700 lines (long) |
| 0 | >700 lines (too long) |

### References Usage (5 points)

| Points | Criteria |
|--------|----------|
| 5 | references/ with 2+ files, referenced in main |
| 3 | references/ with 1+ files |
| 3 | Short file (references not needed) |
| 1 | references/ exists but empty |
| 0 | Long file without references |

### No Duplicate Content (2 points)

| Points | Criteria |
|--------|----------|
| 2 | No duplicate paragraphs |
| 0 | Duplicate content found |

---

## Category 5: Examples (10 points)

### Number of Examples (5 points)

Count `## Example` headers and `Example:` patterns

| Points | Criteria |
|--------|----------|
| 5 | 3+ examples |
| 3 | 1-2 examples |
| 0 | No examples |

### Expected Output (3 points)

Look for: output, result, returns, produces, expected

| Points | Criteria |
|--------|----------|
| 3 | Multiple examples show expected output |
| 1 | Some examples show output |
| 0 | No expected outputs shown |

### Realistic Examples (2 points)

Placeholder patterns: foo, bar, baz, xxx, example.com, lorem

| Points | Criteria |
|--------|----------|
| 2 | No/minimal placeholders |
| 1 | Some placeholder text |
| 0 | Many placeholders |

---

## Category 6: Cross-Platform (10 points)

### agentskills.io Fields (5 points)

Fields and weights:
- version: 1 point
- platforms: 1.5 points
- inputs: 1 point
- outputs: 1 point
- tags: 0.5 points

| Points | Criteria |
|--------|----------|
| 5 | Full compliance (4+ field points) |
| 2-4 | Partial compliance |
| 0 | No agentskills.io fields |

### manifest.json (3 points)

| Points | Criteria |
|--------|----------|
| 3 | Valid manifest.json with name + description |
| 1 | manifest.json exists but incomplete |
| 0 | No manifest.json |

### Platform-Agnostic Content (2 points)

Claude-specific terms: claude code, claude-code, anthropic

| Points | Criteria |
|--------|----------|
| 2 | 0-2 Claude-specific references |
| 1 | 3-5 Claude-specific references |
| 0 | >5 Claude-specific references |

---

## Score Calculation

```python
total_score = (
    structure_score +      # max 15
    description_score +    # max 25
    content_score +        # max 25
    disclosure_score +     # max 15
    examples_score +       # max 10
    crossplatform_score    # max 10
)
```

---

## Improvement Strategies

### Quick Wins (High Impact, Low Effort)

1. Add trigger phrases (+8 points)
2. Add more code examples (+4-6 points)
3. Create 2+ examples with output (+5 points)

### Medium Effort

1. Create references/ structure (+4-5 points)
2. Rewrite in imperative form (+3-5 points)
3. Add tables for structured info (+2-4 points)

### Comprehensive

1. Add agentskills.io fields (+5 points)
2. Create manifest.json (+3 points)
3. Full restructuring for disclosure (+8 points)

---

## Using the Scorer

### Command Line

```bash
# Basic scoring
python3 scripts/score-skill.py /path/to/skill

# With minimum threshold
python3 scripts/score-skill.py /path/to/skill --min-score 80

# JSON output
python3 scripts/score-skill.py /path/to/skill --json
```

### In Claude Code

```
/skill-score ~/.claude/skills/my-skill
```

### CI Integration

```yaml
- name: Check skill quality
  run: |
    python3 scripts/score-skill.py . --min-score 80 --json
```
