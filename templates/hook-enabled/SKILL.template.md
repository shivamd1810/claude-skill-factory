---
name: {{SKILL_NAME}}
description: |
  {{DESCRIPTION_LINE_1}}
  Automated hooks for: {{HOOK_PURPOSE}}
  Triggers for: "{{TRIGGER_1}}", "{{TRIGGER_2}}", "{{TRIGGER_3}}"
hooks:
  - type: PreToolUse
    tool: {{PRE_TOOL_NAME}}
    script: scripts/{{PRE_HOOK_SCRIPT}}
  - type: PostToolUse
    tool: {{POST_TOOL_NAME}}
    script: scripts/{{POST_HOOK_SCRIPT}}
---

# {{SKILL_TITLE}}

{{BRIEF_INTRODUCTION}}

## Hook Overview

This skill provides automated hooks that trigger before or after specific tool operations.

### Active Hooks

| Hook Type | Tool | Script | Purpose |
|-----------|------|--------|---------|
| PreToolUse | {{PRE_TOOL_NAME}} | `scripts/{{PRE_HOOK_SCRIPT}}` | {{PRE_HOOK_PURPOSE}} |
| PostToolUse | {{POST_TOOL_NAME}} | `scripts/{{POST_HOOK_SCRIPT}}` | {{POST_HOOK_PURPOSE}} |

## Hook Behavior

### Pre-Tool Hook: {{PRE_HOOK_NAME}}

**Triggers:** Before every `{{PRE_TOOL_NAME}}` operation

**Actions:**
1. {{PRE_ACTION_1}}
2. {{PRE_ACTION_2}}
3. {{PRE_ACTION_3}}

**Script behavior:**
```bash
# scripts/{{PRE_HOOK_SCRIPT}}
{{PRE_HOOK_SCRIPT_CONTENT}}
```

**Exit codes:**
| Code | Meaning | Effect |
|------|---------|--------|
| 0 | Success | Tool proceeds normally |
| 1 | Warning | Tool proceeds with warning |
| 2 | Block | Tool execution blocked |

---

### Post-Tool Hook: {{POST_HOOK_NAME}}

**Triggers:** After every `{{POST_TOOL_NAME}}` operation

**Actions:**
1. {{POST_ACTION_1}}
2. {{POST_ACTION_2}}
3. {{POST_ACTION_3}}

**Script behavior:**
```bash
# scripts/{{POST_HOOK_SCRIPT}}
{{POST_HOOK_SCRIPT_CONTENT}}
```

**Input:** Receives tool output via stdin

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `{{ENV_VAR_1}}` | {{ENV_VAR_1_DESC}} | `{{ENV_VAR_1_DEFAULT}}` |
| `{{ENV_VAR_2}}` | {{ENV_VAR_2_DESC}} | `{{ENV_VAR_2_DEFAULT}}` |

### Config File

Create `{{CONFIG_FILE}}` to customize behavior:

```{{CONFIG_FORMAT}}
{{CONFIG_CONTENT}}
```

## Hook Data Format

### PreToolUse Input

```json
{
  "tool": "{{PRE_TOOL_NAME}}",
  "parameters": {
    {{PRE_TOOL_PARAMS}}
  }
}
```

### PostToolUse Input

```json
{
  "tool": "{{POST_TOOL_NAME}}",
  "parameters": {
    {{POST_TOOL_PARAMS}}
  },
  "result": {{POST_TOOL_RESULT}}
}
```

## Examples

### Example 1: {{EXAMPLE_1_TITLE}}

**Scenario:** {{EXAMPLE_1_SCENARIO}}

**Hook triggers:**
```
{{EXAMPLE_1_TRIGGER}}
```

**Hook output:**
```
{{EXAMPLE_1_OUTPUT}}
```

### Example 2: {{EXAMPLE_2_TITLE}}

**Scenario:** {{EXAMPLE_2_SCENARIO}}

**Hook triggers:**
```
{{EXAMPLE_2_TRIGGER}}
```

**Hook output:**
```
{{EXAMPLE_2_OUTPUT}}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Hook not triggering | {{ISSUE_1_CAUSE}} | {{ISSUE_1_SOLUTION}} |
| Hook blocking incorrectly | {{ISSUE_2_CAUSE}} | {{ISSUE_2_SOLUTION}} |
| Performance slowdown | {{ISSUE_3_CAUSE}} | {{ISSUE_3_SOLUTION}} |

## Disabling Hooks

To temporarily disable hooks:

```bash
{{DISABLE_HOOK_COMMAND}}
```

To re-enable:

```bash
{{ENABLE_HOOK_COMMAND}}
```

## References

- `references/hook-specification.md` - Detailed hook API
- `references/script-examples.md` - More script patterns

---

<!--
TEMPLATE: hook-enabled
USE FOR: Skills that automate actions via PreToolUse/PostToolUse hooks
CHARACTERISTICS:
- Defines hooks in frontmatter
- Scripts that run automatically on tool events
- Can inspect, modify, or block tool operations
- Requires executable scripts in scripts/

DIRECTORY STRUCTURE:
{{SKILL_NAME}}/
├── SKILL.md
├── scripts/
│   ├── {{PRE_HOOK_SCRIPT}}   # Must be executable
│   └── {{POST_HOOK_SCRIPT}}  # Must be executable
└── references/
    ├── hook-specification.md
    └── script-examples.md

HOOK TYPES:
- PreToolUse: Runs BEFORE tool execution (can block)
- PostToolUse: Runs AFTER tool execution (can process output)

COMMON USE CASES:
- Auto-formatting code after edits
- Validating changes before commits
- Logging tool usage
- Adding boilerplate automatically
-->
