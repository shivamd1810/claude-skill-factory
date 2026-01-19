---
name: {{SKILL_NAME}}
description: |
  {{DESCRIPTION_LINE_1}}
  Integrates with: {{TOOL_NAME}}
  Triggers for: "{{TRIGGER_1}}", "{{TRIGGER_2}}", "{{TRIGGER_3}}"
---

# {{SKILL_TITLE}}

{{BRIEF_INTRODUCTION}}

## Tool Information

| Property | Value |
|----------|-------|
| Tool | {{TOOL_NAME}} |
| Version | {{TOOL_VERSION}} |
| Documentation | {{TOOL_DOCS_URL}} |
| Installation | {{INSTALLATION_COMMAND}} |

## Prerequisites

Ensure the tool is available:

```bash
{{CHECK_TOOL_COMMAND}}
```

**Expected output:** {{EXPECTED_VERSION_OUTPUT}}

If not installed:
```bash
{{INSTALL_COMMAND}}
```

## Common Operations

### {{OPERATION_1_NAME}}

**Purpose:** {{OPERATION_1_PURPOSE}}

**Command:**
```bash
{{OPERATION_1_COMMAND}}
```

**Options:**
| Flag | Description |
|------|-------------|
| `{{FLAG_1}}` | {{FLAG_1_DESC}} |
| `{{FLAG_2}}` | {{FLAG_2_DESC}} |

**Example:**
```bash
{{OPERATION_1_EXAMPLE}}
```

---

### {{OPERATION_2_NAME}}

**Purpose:** {{OPERATION_2_PURPOSE}}

**Command:**
```bash
{{OPERATION_2_COMMAND}}
```

**Example:**
```bash
{{OPERATION_2_EXAMPLE}}
```

---

### {{OPERATION_3_NAME}}

**Purpose:** {{OPERATION_3_PURPOSE}}

**Command:**
```bash
{{OPERATION_3_COMMAND}}
```

**Example:**
```bash
{{OPERATION_3_EXAMPLE}}
```

## Workflows

### Workflow: {{WORKFLOW_1_NAME}}

{{WORKFLOW_1_DESCRIPTION}}

```bash
# Step 1: {{WORKFLOW_1_STEP_1}}
{{WORKFLOW_1_COMMAND_1}}

# Step 2: {{WORKFLOW_1_STEP_2}}
{{WORKFLOW_1_COMMAND_2}}

# Step 3: {{WORKFLOW_1_STEP_3}}
{{WORKFLOW_1_COMMAND_3}}
```

### Workflow: {{WORKFLOW_2_NAME}}

{{WORKFLOW_2_DESCRIPTION}}

```bash
{{WORKFLOW_2_COMMANDS}}
```

## Configuration

### Config File Location

```
{{CONFIG_FILE_PATH}}
```

### Recommended Settings

```{{CONFIG_FORMAT}}
{{RECOMMENDED_CONFIG}}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `{{ERROR_1}}` | {{CAUSE_1}} | {{SOLUTION_1}} |
| `{{ERROR_2}}` | {{CAUSE_2}} | {{SOLUTION_2}} |
| `{{ERROR_3}}` | {{CAUSE_3}} | {{SOLUTION_3}} |

## Scripts

Helper scripts are available in `scripts/`:

- `scripts/{{SCRIPT_1}}.sh` - {{SCRIPT_1_DESC}}
- `scripts/{{SCRIPT_2}}.sh` - {{SCRIPT_2_DESC}}

## References

- `references/command-reference.md` - Full command documentation
- `references/configuration.md` - All configuration options
- {{TOOL_DOCS_URL}} - Official documentation

---

<!--
TEMPLATE: tool-integration
USE FOR: Wrapping external CLI tools or APIs
CHARACTERISTICS:
- Documents tool installation and verification
- Common operations with flags and options
- Multi-step workflows combining commands
- Error handling for tool-specific issues
- Helper scripts for complex operations

DIRECTORY STRUCTURE:
{{SKILL_NAME}}/
├── SKILL.md
├── references/
│   ├── command-reference.md
│   └── configuration.md
└── scripts/
    ├── {{SCRIPT_1}}.sh
    └── {{SCRIPT_2}}.sh
-->
