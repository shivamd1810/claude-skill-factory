---
# agentskills.io compatible frontmatter
name: {{SKILL_NAME}}
version: "1.0.0"
description: |
  {{DESCRIPTION_LINE_1}}
  Cross-platform skill for: {{CROSS_PLATFORM_PURPOSE}}
  Triggers for: "{{TRIGGER_1}}", "{{TRIGGER_2}}", "{{TRIGGER_3}}"
author: {{AUTHOR_NAME}}
license: MIT
platforms:
  - claude-code
  - gemini-cli
  - cursor
  - aider
  - continue
tags:
  - {{TAG_1}}
  - {{TAG_2}}
  - {{TAG_3}}
inputs:
  - name: {{INPUT_1_NAME}}
    type: {{INPUT_1_TYPE}}
    description: {{INPUT_1_DESC}}
    required: {{INPUT_1_REQUIRED}}
  - name: {{INPUT_2_NAME}}
    type: {{INPUT_2_TYPE}}
    description: {{INPUT_2_DESC}}
    required: {{INPUT_2_REQUIRED}}
outputs:
  - name: {{OUTPUT_1_NAME}}
    type: {{OUTPUT_1_TYPE}}
    description: {{OUTPUT_1_DESC}}
---

# {{SKILL_TITLE}}

{{BRIEF_INTRODUCTION}}

## Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Fully supported | Native skill format |
| Gemini CLI | Fully supported | Uses standard markdown |
| Cursor | Fully supported | Place in `.cursor/skills/` |
| Aider | Partially supported | Use as context file |
| Continue | Fully supported | Configure in `config.json` |

## Installation

### Claude Code
```bash
# Personal installation
cp -r {{SKILL_NAME}}/ ~/.claude/skills/

# Project installation
cp -r {{SKILL_NAME}}/ .claude/skills/
```

### Gemini CLI
```bash
cp -r {{SKILL_NAME}}/ ~/.gemini/skills/
```

### Cursor
```bash
cp -r {{SKILL_NAME}}/ .cursor/skills/
```

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `{{INPUT_1_NAME}}` | {{INPUT_1_TYPE}} | {{INPUT_1_REQUIRED}} | {{INPUT_1_DESC}} |
| `{{INPUT_2_NAME}}` | {{INPUT_2_TYPE}} | {{INPUT_2_REQUIRED}} | {{INPUT_2_DESC}} |

### Input Format

```json
{
  "{{INPUT_1_NAME}}": {{INPUT_1_EXAMPLE}},
  "{{INPUT_2_NAME}}": {{INPUT_2_EXAMPLE}}
}
```

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `{{OUTPUT_1_NAME}}` | {{OUTPUT_1_TYPE}} | {{OUTPUT_1_DESC}} |

### Output Format

```json
{
  "{{OUTPUT_1_NAME}}": {{OUTPUT_1_EXAMPLE}}
}
```

## Usage

### Basic Usage

{{BASIC_USAGE_DESCRIPTION}}

**Example prompt:**
```
{{BASIC_USAGE_PROMPT}}
```

**Expected behavior:**
{{BASIC_USAGE_BEHAVIOR}}

### Advanced Usage

{{ADVANCED_USAGE_DESCRIPTION}}

**Example prompt:**
```
{{ADVANCED_USAGE_PROMPT}}
```

## Core Instructions

{{CORE_INSTRUCTIONS}}

### Step 1: {{STEP_1_TITLE}}

{{STEP_1_CONTENT}}

### Step 2: {{STEP_2_TITLE}}

{{STEP_2_CONTENT}}

### Step 3: {{STEP_3_TITLE}}

{{STEP_3_CONTENT}}

## Examples

### Example 1: {{EXAMPLE_1_TITLE}}

**Input:**
```json
{{EXAMPLE_1_INPUT}}
```

**Process:**
{{EXAMPLE_1_PROCESS}}

**Output:**
```json
{{EXAMPLE_1_OUTPUT}}
```

### Example 2: {{EXAMPLE_2_TITLE}}

**Input:**
```json
{{EXAMPLE_2_INPUT}}
```

**Process:**
{{EXAMPLE_2_PROCESS}}

**Output:**
```json
{{EXAMPLE_2_OUTPUT}}
```

## Platform-Specific Notes

### Claude Code

{{CLAUDE_CODE_NOTES}}

### Gemini CLI

{{GEMINI_CLI_NOTES}}

### Cursor

{{CURSOR_NOTES}}

## Manifest File

For agentskills.io registry, include `manifest.json`:

```json
{
  "name": "{{SKILL_NAME}}",
  "version": "1.0.0",
  "description": "{{DESCRIPTION_LINE_1}}",
  "author": "{{AUTHOR_NAME}}",
  "license": "MIT",
  "platforms": ["claude-code", "gemini-cli", "cursor", "aider", "continue"],
  "tags": ["{{TAG_1}}", "{{TAG_2}}", "{{TAG_3}}"],
  "repository": "{{REPOSITORY_URL}}",
  "skill_file": "SKILL.md"
}
```

## References

- `references/platform-guides.md` - Platform-specific setup
- `references/api-specification.md` - Detailed I/O spec
- `manifest.json` - agentskills.io manifest

---

<!--
TEMPLATE: cross-platform
USE FOR: Skills designed to work across multiple AI coding assistants
CHARACTERISTICS:
- agentskills.io compliant frontmatter
- Platform compatibility matrix
- Explicit inputs/outputs specification
- Installation instructions per platform
- Manifest file for registry

DIRECTORY STRUCTURE:
{{SKILL_NAME}}/
├── SKILL.md
├── manifest.json              # agentskills.io manifest
└── references/
    ├── platform-guides.md
    └── api-specification.md

AGENTSKILLS.IO SPECIFICATION:
- name: lowercase-with-dashes
- version: semver format
- platforms: array of supported platforms
- inputs: array of typed parameters
- outputs: array of typed results
- tags: for discovery

SUPPORTED PLATFORMS:
- claude-code: Anthropic's Claude Code CLI
- gemini-cli: Google's Gemini CLI
- cursor: Cursor AI editor
- aider: Aider CLI tool
- continue: Continue VS Code extension
-->
