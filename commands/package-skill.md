---
name: package-skill
description: Create distribution-ready ZIP package for a Claude Code skill
args: <path>
---

# Package Skill Command

Create a distribution-ready package for sharing your Claude Code skill with others.

## Usage

```
/package-skill <path-to-skill>
```

**Arguments:**
- `<path>` - Path to skill directory or SKILL.md file

**Options:**
- `-o, --output` - Output directory (default: skill's parent directory)

## What Gets Packaged

The packager creates a ZIP file containing:

| File | Source |
|------|--------|
| `SKILL.md` | Your main skill file |
| `references/` | Your reference documentation |
| `scripts/` | Your automation scripts |
| `manifest.json` | Generated if not present (agentskills.io format) |
| `README.md` | Generated if not present (installation instructions) |

## Packaging Process

When this command is invoked:

1. **Validate the skill exists** at the provided path

2. **Run the packaging script**:
   ```bash
   python3 scripts/package-skill.py <path>
   ```

3. **Collect all skill files**:
   - Excludes hidden files (`.DS_Store`, etc.)
   - Excludes Python cache (`__pycache__`, `.pyc`)
   - Preserves directory structure

4. **Generate missing files**:
   - `manifest.json` for agentskills.io registry
   - `README.md` with installation instructions

5. **Create ZIP archive**:
   - Named: `{skill-name}-{version}.zip`
   - Compressed for smaller size

## Example Output

```
> /package-skill ~/.claude/skills/my-skill

Packaging skill: my-skill
Version: 1.0.0
Output: /Users/you/.claude/skills/my-skill-1.0.0.zip

  Added: my-skill/SKILL.md
  Added: my-skill/references/guide.md
  Added: my-skill/scripts/helper.py
  Generated: my-skill/manifest.json
  Generated: my-skill/README.md

Package created: /Users/you/.claude/skills/my-skill-1.0.0.zip
Size: 12.5 KB

=== Package Summary ===

Contents:
  my-skill/SKILL.md (2048 bytes)
  my-skill/references/guide.md (4096 bytes)
  my-skill/scripts/helper.py (1024 bytes)
  my-skill/manifest.json (512 bytes)
  my-skill/README.md (1024 bytes)

=== Distribution Options ===

1. Share directly:
   Send my-skill-1.0.0.zip to others

2. Publish to GitHub:
   Create a repo named 'my-skill'
   Unzip and push the contents

3. Submit to agentskills.io registry:
   Visit https://agentskills.io/submit
   Upload the manifest.json

=== Installation Command ===

unzip my-skill-1.0.0.zip -d ~/.claude/skills/
```

## Generated manifest.json

The auto-generated manifest follows the agentskills.io specification:

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "Short description from SKILL.md",
  "author": "Unknown",
  "license": "MIT",
  "platforms": ["claude-code"],
  "tags": ["extracted", "from", "content"],
  "skill_file": "SKILL.md",
  "created": "2025-01-15T12:00:00"
}
```

To customize, add these fields to your SKILL.md frontmatter:
- `version: "1.0.0"`
- `author: "Your Name"`
- `license: "MIT"`
- `platforms: ["claude-code", "gemini-cli"]`
- `tags: ["tag1", "tag2"]`

## Generated README.md

The auto-generated README includes:
- Skill name and description
- Installation instructions for Claude Code
- Usage information (trigger phrases)
- File listing
- License information

## Distribution Options

After packaging:

### Option 1: Direct Sharing
Send the ZIP file via email, Slack, etc.

Recipients install with:
```bash
unzip my-skill-1.0.0.zip -d ~/.claude/skills/
```

### Option 2: GitHub Repository
1. Create a new GitHub repository
2. Unzip the package
3. Push the contents
4. Share the repo URL

Users can then:
```bash
git clone https://github.com/you/my-skill ~/.claude/skills/my-skill
```

### Option 3: agentskills.io Registry
1. Visit https://agentskills.io/submit
2. Upload your `manifest.json`
3. Link to your GitHub repo or ZIP
4. Your skill becomes discoverable

## JSON Output

For automation:

```bash
python3 scripts/package-skill.py <path> --json
```

Returns:
```json
{
  "success": true,
  "package_path": "/path/to/my-skill-1.0.0.zip",
  "size_bytes": 12800,
  "skill_name": "my-skill",
  "version": "1.0.0"
}
```

## Before Packaging

Run these commands first:

1. **Validate**: `/validate-skill <path>` - Ensure skill follows best practices
2. **Score**: `/skill-score <path>` - Aim for score >= 80

## Related Commands

- `/create-skill` - Create a new skill
- `/validate-skill <path>` - Validate before packaging
- `/skill-score <path>` - Check quality score
