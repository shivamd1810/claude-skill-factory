---
name: {{SKILL_NAME}}
description: |
  {{DESCRIPTION_LINE_1}}
  Use when: {{USE_CONDITION}}
  Triggers for: "{{TRIGGER_1}}", "{{TRIGGER_2}}", "{{TRIGGER_3}}"
---

# {{SKILL_TITLE}}

{{BRIEF_INTRODUCTION}}

## Workflow Overview

```
{{WORKFLOW_DIAGRAM}}
```

## Prerequisites

Before starting, ensure:
- [ ] {{PREREQ_1}}
- [ ] {{PREREQ_2}}
- [ ] {{PREREQ_3}}

## Workflow Steps

### Step 1: {{STEP_1_TITLE}}

**Goal:** {{STEP_1_GOAL}}

**Actions:**
1. {{STEP_1_ACTION_1}}
2. {{STEP_1_ACTION_2}}

**Verification:**
```{{LANGUAGE}}
{{STEP_1_VERIFY_COMMAND}}
```

**Expected output:** {{STEP_1_EXPECTED}}

**If failed:** {{STEP_1_FALLBACK}}

---

### Step 2: {{STEP_2_TITLE}}

**Goal:** {{STEP_2_GOAL}}

**Actions:**
1. {{STEP_2_ACTION_1}}
2. {{STEP_2_ACTION_2}}

**Verification:**
```{{LANGUAGE}}
{{STEP_2_VERIFY_COMMAND}}
```

**Expected output:** {{STEP_2_EXPECTED}}

**If failed:** {{STEP_2_FALLBACK}}

---

### Step 3: {{STEP_3_TITLE}}

**Goal:** {{STEP_3_GOAL}}

**Actions:**
1. {{STEP_3_ACTION_1}}
2. {{STEP_3_ACTION_2}}

**Verification:**
```{{LANGUAGE}}
{{STEP_3_VERIFY_COMMAND}}
```

**Expected output:** {{STEP_3_EXPECTED}}

**If failed:** {{STEP_3_FALLBACK}}

---

### Step 4: {{STEP_4_TITLE}}

**Goal:** {{STEP_4_GOAL}}

**Actions:**
1. {{STEP_4_ACTION_1}}
2. {{STEP_4_ACTION_2}}

**Verification:**
```{{LANGUAGE}}
{{STEP_4_VERIFY_COMMAND}}
```

**Expected output:** {{STEP_4_EXPECTED}}

## Decision Points

### Decision: {{DECISION_1_TITLE}}

**Condition:** {{DECISION_1_CONDITION}}

| If... | Then... |
|-------|---------|
| {{DECISION_1_IF_1}} | {{DECISION_1_THEN_1}} |
| {{DECISION_1_IF_2}} | {{DECISION_1_THEN_2}} |

## Rollback Procedures

If the workflow fails at any step:

### Rollback from Step {{N}}

```{{LANGUAGE}}
{{ROLLBACK_COMMANDS}}
```

## Completion Checklist

After completing the workflow:
- [ ] {{COMPLETION_CHECK_1}}
- [ ] {{COMPLETION_CHECK_2}}
- [ ] {{COMPLETION_CHECK_3}}

## References

- `references/detailed-steps.md` - Step-by-step with screenshots
- `references/troubleshooting.md` - Common issues and solutions
- `scripts/{{HELPER_SCRIPT}}` - Automation helper

---

<!--
TEMPLATE: workflow
USE FOR: Multi-step processes with verification and rollback
CHARACTERISTICS:
- Sequential steps with clear verification
- Decision points for branching logic
- Rollback procedures for failure recovery
- Checklists for prerequisites and completion

WORKFLOW_DIAGRAM example:
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Step 1  │───▶│ Step 2  │───▶│ Step 3  │
└─────────┘    └────┬────┘    └─────────┘
                    │
                    ▼ (if condition)
               ┌─────────┐
               │ Step 2b │
               └─────────┘

DIRECTORY STRUCTURE:
{{SKILL_NAME}}/
├── SKILL.md
├── references/
│   ├── detailed-steps.md
│   └── troubleshooting.md
└── scripts/
    └── {{HELPER_SCRIPT}}
-->
