#!/usr/bin/env python3
"""
Skill Packager - Create distribution-ready packages for Claude Code skills

Creates a ZIP file with:
- All skill files
- Generated README.md (if not present)
- manifest.json for agentskills.io
- Installation instructions
"""

import os
import sys
import re
import json
import zipfile
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def colorize(text: str, color: str) -> str:
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.END}"
    return text

class SkillPackager:
    """Package Claude Code skills for distribution."""

    def __init__(self, skill_path: str, output_dir: str = None):
        self.skill_path = Path(skill_path).resolve()
        self.output_dir = Path(output_dir).resolve() if output_dir else self.skill_path.parent
        self.skill_md_path = None
        self.content = ""
        self.frontmatter = {}
        self.body = ""

    def find_skill_file(self) -> bool:
        """Locate the SKILL.md file."""
        if self.skill_path.is_file() and self.skill_path.name == "SKILL.md":
            self.skill_md_path = self.skill_path
            self.skill_path = self.skill_path.parent
        elif self.skill_path.is_dir():
            skill_file = self.skill_path / "SKILL.md"
            if skill_file.exists():
                self.skill_md_path = skill_file
        return self.skill_md_path is not None

    def parse_frontmatter(self) -> bool:
        """Parse YAML frontmatter from SKILL.md."""
        try:
            with open(self.skill_md_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except Exception:
            return False

        if not self.content.startswith('---'):
            self.body = self.content
            return True

        parts = self.content.split('---', 2)
        if len(parts) < 3:
            self.body = self.content
            return True

        frontmatter_text = parts[1].strip()
        self.body = parts[2].strip()

        # Simple YAML parsing
        current_key = None
        current_value = []
        in_multiline = False

        for line in frontmatter_text.split('\n'):
            if not line.startswith(' ') and ':' in line:
                if current_key and in_multiline:
                    self.frontmatter[current_key] = '\n'.join(current_value)

                key_part = line.split(':', 1)
                current_key = key_part[0].strip()
                value = key_part[1].strip() if len(key_part) > 1 else ""

                if value == '|':
                    in_multiline = True
                    current_value = []
                elif value.startswith('[') or value.startswith('{'):
                    self.frontmatter[current_key] = value
                    current_key = None
                elif value:
                    self.frontmatter[current_key] = value.strip('"\'')
                    current_key = None
                else:
                    in_multiline = False
                    current_value = []
            elif current_key and in_multiline:
                current_value.append(line.strip())

        if current_key and in_multiline:
            self.frontmatter[current_key] = '\n'.join(current_value)

        return True

    def generate_manifest(self) -> Dict:
        """Generate agentskills.io manifest."""
        name = self.frontmatter.get('name', self.skill_path.name)
        description = self.frontmatter.get('description', '')

        # Extract first line of description for short desc
        short_desc = description.split('\n')[0].strip() if description else f"{name} skill"

        manifest = {
            "name": name,
            "version": self.frontmatter.get('version', '1.0.0').strip('"'),
            "description": short_desc,
            "author": self.frontmatter.get('author', 'Unknown'),
            "license": self.frontmatter.get('license', 'MIT'),
            "platforms": ["claude-code"],
            "tags": [],
            "skill_file": "SKILL.md",
            "created": datetime.now().isoformat(),
        }

        # Extract tags from frontmatter or generate from description
        if 'tags' in self.frontmatter:
            tags_str = self.frontmatter['tags']
            if tags_str.startswith('['):
                # Try to parse as JSON array
                try:
                    manifest['tags'] = json.loads(tags_str.replace("'", '"'))
                except:
                    pass
        else:
            # Generate tags from name and description
            words = re.findall(r'\b[a-z]{3,}\b', (name + ' ' + description).lower())
            common_words = {'the', 'and', 'for', 'when', 'use', 'this', 'that', 'with'}
            tags = [w for w in words if w not in common_words][:5]
            manifest['tags'] = list(set(tags))

        # Add platforms if specified
        if 'platforms' in self.frontmatter:
            platforms_str = self.frontmatter['platforms']
            if platforms_str.startswith('['):
                try:
                    manifest['platforms'] = json.loads(platforms_str.replace("'", '"'))
                except:
                    pass

        return manifest

    def generate_readme(self) -> str:
        """Generate README.md for the package."""
        name = self.frontmatter.get('name', self.skill_path.name)
        description = self.frontmatter.get('description', '')

        # Extract first paragraph as short description
        short_desc = description.split('\n')[0].strip() if description else ""

        readme = f"""# {name}

{short_desc}

## Installation

### Claude Code (Personal)

```bash
# Clone or copy to your skills directory
cp -r {name}/ ~/.claude/skills/{name}/
```

### Claude Code (Project)

```bash
# Add to your project
cp -r {name}/ .claude/skills/{name}/
```

### Other Platforms

See the `manifest.json` for agentskills.io compatibility information.

## Usage

"""
        # Extract trigger phrases from description
        trigger_match = re.search(r'[Tt]riggers?\s+for[:\s]+(.+)', description)
        if trigger_match:
            triggers = trigger_match.group(1).strip()
            readme += f"""This skill activates when you mention:
{triggers}

"""

        # Add basic usage
        readme += f"""Simply ask Claude to help with tasks related to {name.replace('-', ' ')}.

## Files

```
{name}/
├── SKILL.md              # Main skill file
"""
        # List other directories
        for subdir in ['references', 'scripts']:
            dir_path = self.skill_path / subdir
            if dir_path.exists():
                readme += f"├── {subdir}/\n"
                for f in dir_path.iterdir():
                    if not f.name.startswith('.'):
                        readme += f"│   └── {f.name}\n"

        readme += """```

## License

"""
        license_name = self.frontmatter.get('license', 'MIT')
        readme += f"This skill is released under the {license_name} License.\n"

        return readme

    def collect_files(self) -> List[Path]:
        """Collect all files to include in package."""
        files = []

        # Walk the skill directory
        for item in self.skill_path.rglob('*'):
            if item.is_file():
                # Skip unwanted files
                if item.name.startswith('.'):
                    continue
                if item.name in ['__pycache__', '.DS_Store', 'Thumbs.db']:
                    continue
                if item.suffix in ['.pyc', '.pyo']:
                    continue

                files.append(item)

        return files

    def package(self) -> Optional[Path]:
        """Create the distribution package."""
        if not self.find_skill_file():
            print(colorize("Error: SKILL.md not found", Colors.RED))
            return None

        if not self.parse_frontmatter():
            print(colorize("Error: Could not parse SKILL.md", Colors.RED))
            return None

        name = self.frontmatter.get('name', self.skill_path.name)
        version = self.frontmatter.get('version', '1.0.0').strip('"')

        # Create output filename
        safe_name = re.sub(r'[^a-z0-9-]', '-', name.lower())
        zip_name = f"{safe_name}-{version}.zip"
        zip_path = self.output_dir / zip_name

        print(colorize(f"\nPackaging skill: {name}", Colors.BOLD))
        print(f"Version: {version}")
        print(f"Output: {zip_path}\n")

        # Collect files
        files = self.collect_files()

        # Create ZIP
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Add skill files
                for file_path in files:
                    arcname = f"{name}/{file_path.relative_to(self.skill_path)}"
                    zf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

                # Add manifest.json if not present
                manifest_path = self.skill_path / "manifest.json"
                if not manifest_path.exists():
                    manifest = self.generate_manifest()
                    manifest_content = json.dumps(manifest, indent=2)
                    zf.writestr(f"{name}/manifest.json", manifest_content)
                    print(f"  Generated: {name}/manifest.json")

                # Add README.md if not present
                readme_path = self.skill_path / "README.md"
                if not readme_path.exists():
                    readme = self.generate_readme()
                    zf.writestr(f"{name}/README.md", readme)
                    print(f"  Generated: {name}/README.md")

            print(colorize(f"\nPackage created: {zip_path}", Colors.GREEN))
            print(f"Size: {zip_path.stat().st_size / 1024:.1f} KB")

            return zip_path

        except Exception as e:
            print(colorize(f"Error creating package: {e}", Colors.RED))
            return None

    def print_summary(self, zip_path: Path):
        """Print package summary and next steps."""
        name = self.frontmatter.get('name', self.skill_path.name)

        print(colorize("\n=== Package Summary ===\n", Colors.BOLD))

        # List contents
        print("Contents:")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for info in zf.infolist():
                print(f"  {info.filename} ({info.file_size} bytes)")

        print(colorize("\n=== Distribution Options ===\n", Colors.BOLD))

        print("1. Share directly:")
        print(f"   Send {zip_path.name} to others")
        print()
        print("2. Publish to GitHub:")
        print(f"   Create a repo named '{name}'")
        print("   Unzip and push the contents")
        print()
        print("3. Submit to agentskills.io registry:")
        print("   Visit https://agentskills.io/submit")
        print("   Upload the manifest.json")
        print()

        print(colorize("=== Installation Command ===\n", Colors.BOLD))
        print(f"unzip {zip_path.name} -d ~/.claude/skills/")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Package Claude Code skill for distribution"
    )
    parser.add_argument(
        "path",
        help="Path to skill directory or SKILL.md file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory for the package (default: skill parent directory)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )

    args = parser.parse_args()

    packager = SkillPackager(args.path, args.output)
    zip_path = packager.package()

    if args.json:
        if zip_path:
            output = {
                "success": True,
                "package_path": str(zip_path),
                "size_bytes": zip_path.stat().st_size,
                "skill_name": packager.frontmatter.get('name', packager.skill_path.name),
                "version": packager.frontmatter.get('version', '1.0.0')
            }
        else:
            output = {"success": False, "error": "Failed to create package"}
        print(json.dumps(output, indent=2))
    else:
        if zip_path:
            packager.print_summary(zip_path)

    sys.exit(0 if zip_path else 1)

if __name__ == "__main__":
    main()
