---
name: {{SKILL_NAME}}
description: |
  {{DESCRIPTION_LINE_1}}
  Use when: {{USE_CONDITION}}
  Triggers for: "{{TRIGGER_1}}", "{{TRIGGER_2}}", "{{TRIGGER_3}}"
---

# {{SKILL_TITLE}}

{{BRIEF_INTRODUCTION}}

## Overview

{{OVERVIEW_PARAGRAPH}}

## When to Use

| Scenario | Action |
|----------|--------|
| {{SCENARIO_1}} | {{ACTION_1}} |
| {{SCENARIO_2}} | {{ACTION_2}} |
| {{SCENARIO_3}} | {{ACTION_3}} |

## Quick Start

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

## Core Concepts

### {{CONCEPT_1_TITLE}}

{{CONCEPT_1_EXPLANATION}}

### {{CONCEPT_2_TITLE}}

{{CONCEPT_2_EXPLANATION}}

## Examples

### {{EXAMPLE_1_TITLE}}

{{EXAMPLE_1_CONTEXT}}

```{{LANGUAGE}}
{{EXAMPLE_1_CODE}}
```

**Result:** {{EXAMPLE_1_RESULT}}

### {{EXAMPLE_2_TITLE}}

{{EXAMPLE_2_CONTEXT}}

```{{LANGUAGE}}
{{EXAMPLE_2_CODE}}
```

**Result:** {{EXAMPLE_2_RESULT}}

## Common Patterns

### Pattern: {{PATTERN_1_NAME}}

**When:** {{PATTERN_1_WHEN}}

**How:**
```{{LANGUAGE}}
{{PATTERN_1_CODE}}
```

### Pattern: {{PATTERN_2_NAME}}

**When:** {{PATTERN_2_WHEN}}

**How:**
```{{LANGUAGE}}
{{PATTERN_2_CODE}}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| {{ISSUE_1}} | {{SOLUTION_1}} |
| {{ISSUE_2}} | {{SOLUTION_2}} |

## References

For detailed information, see:
- `references/{{REFERENCE_1}}.md` - {{REFERENCE_1_DESC}}
- `references/{{REFERENCE_2}}.md` - {{REFERENCE_2_DESC}}

---

<!--
TEMPLATE: standard
USE FOR: Most skills that need supporting documentation
CHARACTERISTICS:
- Main SKILL.md with references/ folder
- Moderate complexity
- May include scripts/
- 200-400 lines in main file

DIRECTORY STRUCTURE:
{{SKILL_NAME}}/
├── SKILL.md
├── references/
│   ├── {{REFERENCE_1}}.md
│   └── {{REFERENCE_2}}.md
└── scripts/           # Optional
    └── helper.py

PLACEHOLDER GUIDE:
- {{SKILL_NAME}}: lowercase-with-dashes
- {{LANGUAGE}}: Code language (python, javascript, bash, etc.)
- References should contain detailed docs moved from main file
-->
