---
name: skill-score
description: Get quality score (0-100) for a Claude Code skill with detailed breakdown
args: <path>
---

# Skill Score Command

Score a Claude Code skill on quality metrics, providing a detailed breakdown and actionable recommendations.

## Usage

```
/skill-score <path-to-skill>
```

**Arguments:**
- `<path>` - Path to skill directory or SKILL.md file

## Scoring Process

When this command is invoked:

1. **Locate the skill** at the provided path
2. **Run the scoring script**:
   ```bash
   python3 scripts/score-skill.py <path>
   ```
3. **Display score** with visual bar and letter grade
4. **Show category breakdown** with points earned per category
5. **Provide recommendations** for improvement

## Scoring Categories (100 points)

| Category | Points | What It Measures |
|----------|--------|------------------|
| Structure | 15 | Directory layout, file organization |
| Description | 25 | Trigger phrases, specificity, frontmatter |
| Content | 25 | Clarity, formatting, examples, structure |
| Progressive Disclosure | 15 | Main file conciseness, reference usage |
| Examples | 10 | Number, quality, realistic values |
| Cross-Platform | 10 | agentskills.io compliance |

## Grade Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent - ready for distribution |
| 80-89 | B | Good - meets quality standards |
| 70-79 | C | Acceptable - needs improvement |
| 60-69 | D | Below standard - significant work needed |
| <60 | F | Failing - major restructuring required |

## Example Output

```
=== Skill Quality Score ===

Skill: my-skill
Path: /path/to/my-skill

Score: 78.5/100 [████████████████████████████████░░░░░░░░]
Grade: C

Category Breakdown:
------------------------------------------------------------

Structure (12.0/15)
  [████████████████░░░░] 80%
    +5: SKILL.md exists
    +4: references/ directory with content
    +3: scripts/ exists but some not executable
    +0: Contains unwanted files

Description (20.0/25)
  [████████████████░░░░] 80%
    +3: Valid name field
    +5: Description is comprehensive
    +8: Multiple trigger patterns found
    +4: context:fork properly specified

...

Top Recommendations:
  • Make scripts executable: chmod +x scripts/*
  • Remove .DS_Store, __pycache__, etc.
  • Add more code examples
  • Add manifest.json for registry listing

This skill needs some improvements.
```

## Minimum Score Check

To enforce quality gates:

```bash
python3 scripts/score-skill.py <path> --min-score 80
```

Exits with error code 1 if score is below threshold.

## JSON Output

For CI/CD integration:

```bash
python3 scripts/score-skill.py <path> --json
```

Returns:
```json
{
  "skill_path": "/path/to/my-skill",
  "score": 78.5,
  "grade": "C",
  "categories": [
    {
      "name": "Structure",
      "earned": 12.0,
      "max": 15,
      "percentage": 80.0,
      "breakdown": ["..."],
      "recommendations": ["..."]
    }
  ]
}
```

## Improving Your Score

Focus on categories with lowest percentage:

1. **Low Structure score** → Organize files properly, make scripts executable
2. **Low Description score** → Add trigger phrases, be specific
3. **Low Content score** → Use imperative form, add code examples
4. **Low Disclosure score** → Move details to references/
5. **Low Examples score** → Add more realistic examples
6. **Low Cross-Platform score** → Add agentskills.io fields
