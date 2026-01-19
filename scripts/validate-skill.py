#!/usr/bin/env python3
"""
Skill Validator - 7-Point Validation for Claude Code Skills

Validates skills against Anthropic's best practices:
1. Structure - Correct files and directories
2. Frontmatter - Required fields valid
3. Description - Trigger phrases and scenarios
4. Content - Imperative form, examples, length
5. Progressive Disclosure - Main file conciseness
6. Resources - Referenced files exist
7. Cross-Platform - agentskills.io compatibility
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ANSI colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def colorize(text: str, color: str) -> str:
    """Add color to text if terminal supports it."""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.END}"
    return text

class ValidationResult:
    """Container for validation check results."""

    def __init__(self, name: str, passed: bool, message: str, details: List[str] = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or []

    def __str__(self) -> str:
        status = colorize("PASS", Colors.GREEN) if self.passed else colorize("FAIL", Colors.RED)
        result = f"[{status}] {self.name}: {self.message}"
        if self.details:
            for detail in self.details:
                result += f"\n       - {detail}"
        return result

class SkillValidator:
    """Validates Claude Code skills against best practices."""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path).resolve()
        self.skill_md_path = None
        self.content = ""
        self.frontmatter = {}
        self.body = ""
        self.results: List[ValidationResult] = []

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
        except Exception as e:
            return False

        # Check for frontmatter
        if not self.content.startswith('---'):
            self.body = self.content
            return True

        # Extract frontmatter
        parts = self.content.split('---', 2)
        if len(parts) < 3:
            self.body = self.content
            return True

        frontmatter_text = parts[1].strip()
        self.body = parts[2].strip()

        # Simple YAML parsing (handles basic cases)
        current_key = None
        current_value = []
        in_multiline = False

        for line in frontmatter_text.split('\n'):
            # Check for new key
            if not line.startswith(' ') and ':' in line:
                # Save previous key if exists
                if current_key:
                    if in_multiline:
                        self.frontmatter[current_key] = '\n'.join(current_value)

                key_part = line.split(':', 1)
                current_key = key_part[0].strip()
                value = key_part[1].strip() if len(key_part) > 1 else ""

                if value == '|':
                    in_multiline = True
                    current_value = []
                elif value.startswith('[') or value.startswith('{'):
                    # Handle inline arrays/objects
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

        # Save last key
        if current_key and in_multiline:
            self.frontmatter[current_key] = '\n'.join(current_value)

        return True

    def validate_structure(self) -> ValidationResult:
        """Check 1: Validate directory structure."""
        issues = []

        # Check SKILL.md exists
        if not self.skill_md_path or not self.skill_md_path.exists():
            return ValidationResult(
                "Structure",
                False,
                "SKILL.md not found",
                ["Create a SKILL.md file in the skill directory"]
            )

        # Check for common structure issues
        references_dir = self.skill_path / "references"
        scripts_dir = self.skill_path / "scripts"

        # Check if references are mentioned but directory doesn't exist
        if "references/" in self.content and not references_dir.exists():
            issues.append("references/ directory mentioned but doesn't exist")

        # Check if scripts are mentioned but directory doesn't exist
        if "scripts/" in self.content and not scripts_dir.exists():
            issues.append("scripts/ directory mentioned but doesn't exist")

        if issues:
            return ValidationResult("Structure", False, "Structure issues found", issues)

        return ValidationResult("Structure", True, "Directory structure is valid")

    def validate_frontmatter(self) -> ValidationResult:
        """Check 2: Validate frontmatter fields."""
        issues = []

        # Required field: name
        if 'name' not in self.frontmatter:
            issues.append("Missing required 'name' field")
        elif not re.match(r'^[a-z0-9-]+$', self.frontmatter['name']):
            issues.append("'name' should be lowercase with dashes (e.g., 'my-skill')")

        # Required field: description
        if 'description' not in self.frontmatter:
            issues.append("Missing required 'description' field")
        elif len(self.frontmatter.get('description', '')) < 20:
            issues.append("'description' is too short (minimum 20 characters)")

        # Optional but validated: context
        if 'context' in self.frontmatter:
            valid_contexts = ['fork', 'append']
            if self.frontmatter['context'] not in valid_contexts:
                issues.append(f"'context' must be one of: {', '.join(valid_contexts)}")

        if issues:
            return ValidationResult("Frontmatter", False, "Frontmatter issues found", issues)

        return ValidationResult("Frontmatter", True, "Frontmatter is valid")

    def validate_description(self) -> ValidationResult:
        """Check 3: Validate description quality."""
        issues = []
        recommendations = []

        description = self.frontmatter.get('description', '')

        # Check for trigger phrases
        trigger_indicators = ['trigger', 'activates for', 'use when', 'triggers for']
        has_triggers = any(ind.lower() in description.lower() for ind in trigger_indicators)

        if not has_triggers:
            issues.append("No trigger phrases found in description")
            recommendations.append("Add phrases like 'Triggers for: \"phrase1\", \"phrase2\"'")

        # Check for specificity
        generic_words = ['help', 'assist', 'support', 'various', 'many', 'different']
        generic_count = sum(1 for word in generic_words if word in description.lower())

        if generic_count >= 2:
            recommendations.append("Description is too generic - add specific scenarios")

        # Check description length
        if len(description) < 50:
            issues.append("Description too short for effective auto-triggering")

        if issues:
            return ValidationResult("Description", False, "Description quality issues", issues + recommendations)

        if recommendations:
            return ValidationResult("Description", True, "Description valid with recommendations", recommendations)

        return ValidationResult("Description", True, "Description is well-crafted")

    def validate_content(self) -> ValidationResult:
        """Check 4: Validate content quality."""
        issues = []
        recommendations = []

        lines = self.body.split('\n')

        # Check for imperative form (common passive indicators)
        passive_indicators = ['you should', 'you can', 'you will', 'you may', 'it is recommended']
        passive_count = sum(1 for ind in passive_indicators if ind.lower() in self.body.lower())

        if passive_count > 3:
            recommendations.append("Use imperative form more ('Run tests' not 'You should run tests')")

        # Check for examples
        example_indicators = ['example', '```', 'e.g.', 'for instance']
        has_examples = any(ind.lower() in self.body.lower() for ind in example_indicators)

        if not has_examples:
            issues.append("No examples found - add concrete examples with expected outputs")

        # Check for headers (structure)
        header_count = len(re.findall(r'^#{1,3}\s', self.body, re.MULTILINE))

        if header_count < 2:
            recommendations.append("Add more section headers for better organization")

        # Check for code blocks
        code_block_count = self.body.count('```')

        if code_block_count < 2:
            recommendations.append("Consider adding more code examples")

        if issues:
            return ValidationResult("Content", False, "Content quality issues", issues + recommendations)

        if recommendations:
            return ValidationResult("Content", True, "Content valid with recommendations", recommendations)

        return ValidationResult("Content", True, "Content is well-structured")

    def validate_progressive_disclosure(self) -> ValidationResult:
        """Check 5: Validate progressive disclosure."""
        issues = []

        lines = self.content.split('\n')
        line_count = len(lines)

        # Check main file length
        if line_count > 500:
            issues.append(f"SKILL.md is {line_count} lines (recommended: under 500)")
            issues.append("Move detailed documentation to references/ folder")

        # Check for very long sections
        current_section_lines = 0
        for line in lines:
            if line.startswith('#'):
                if current_section_lines > 100:
                    issues.append("Some sections are very long - consider breaking them up")
                    break
                current_section_lines = 0
            else:
                current_section_lines += 1

        # Check if references folder is used appropriately
        references_dir = self.skill_path / "references"
        if line_count > 300 and not references_dir.exists():
            issues.append("Consider using references/ folder for detailed documentation")

        if issues:
            return ValidationResult("Progressive Disclosure", False, "Disclosure issues found", issues)

        return ValidationResult("Progressive Disclosure", True, "Good progressive disclosure")

    def validate_resources(self) -> ValidationResult:
        """Check 6: Validate referenced resources exist."""
        issues = []

        # Find referenced files
        file_patterns = [
            r'`([^`]+\.(?:md|py|sh|js|ts))`',
            r'references/([^\s\)]+)',
            r'scripts/([^\s\)]+)',
        ]

        referenced_files = set()
        for pattern in file_patterns:
            matches = re.findall(pattern, self.content)
            referenced_files.update(matches)

        # Check if referenced files exist
        for ref in referenced_files:
            # Skip template placeholders
            if '{{' in ref:
                continue

            ref_path = self.skill_path / ref
            if not ref_path.exists():
                # Also check without leading path component
                if '/' in ref:
                    alt_path = self.skill_path / ref.split('/')[-1]
                    if not alt_path.exists():
                        issues.append(f"Referenced file not found: {ref}")

        # Check script permissions
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.glob('*.sh'):
                if not os.access(script, os.X_OK):
                    issues.append(f"Script not executable: {script.name}")
            for script in scripts_dir.glob('*.py'):
                if not os.access(script, os.X_OK):
                    issues.append(f"Script not executable: {script.name}")

        if issues:
            return ValidationResult("Resources", False, "Resource issues found", issues)

        return ValidationResult("Resources", True, "All referenced resources exist")

    def validate_cross_platform(self) -> ValidationResult:
        """Check 7: Validate agentskills.io compatibility."""
        issues = []
        recommendations = []

        # Check for agentskills.io fields
        agentskills_fields = ['version', 'platforms', 'inputs', 'outputs', 'tags']
        has_agentskills = any(field in self.frontmatter for field in agentskills_fields)

        if not has_agentskills:
            recommendations.append("Consider adding agentskills.io fields for cross-platform compatibility")
            recommendations.append("Fields: version, platforms, inputs, outputs, tags")
        else:
            # Validate version format
            version = self.frontmatter.get('version', '')
            if version and not re.match(r'^\d+\.\d+\.\d+', version.strip('"')):
                issues.append("'version' should follow semver format (e.g., '1.0.0')")

            # Check for manifest.json
            manifest_path = self.skill_path / "manifest.json"
            if not manifest_path.exists():
                recommendations.append("Consider adding manifest.json for agentskills.io registry")

        if issues:
            return ValidationResult("Cross-Platform", False, "Compatibility issues", issues + recommendations)

        if recommendations:
            return ValidationResult("Cross-Platform", True, "Optional cross-platform improvements", recommendations)

        return ValidationResult("Cross-Platform", True, "Cross-platform compatible")

    def validate(self) -> Tuple[bool, List[ValidationResult]]:
        """Run all validation checks."""

        # Find and parse skill file
        if not self.find_skill_file():
            return False, [ValidationResult(
                "Initialization",
                False,
                "Could not find SKILL.md",
                [f"Searched in: {self.skill_path}"]
            )]

        if not self.parse_frontmatter():
            return False, [ValidationResult(
                "Initialization",
                False,
                "Could not parse SKILL.md",
                ["Check file encoding and format"]
            )]

        # Run all checks
        self.results = [
            self.validate_structure(),
            self.validate_frontmatter(),
            self.validate_description(),
            self.validate_content(),
            self.validate_progressive_disclosure(),
            self.validate_resources(),
            self.validate_cross_platform(),
        ]

        all_passed = all(r.passed for r in self.results)
        return all_passed, self.results

    def print_results(self):
        """Print validation results to console."""
        print(colorize("\n=== Skill Validation Report ===\n", Colors.BOLD))
        print(f"Skill: {self.skill_path.name}")
        print(f"Path: {self.skill_path}\n")

        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        for result in self.results:
            print(result)
            print()

        print(colorize("=== Summary ===", Colors.BOLD))

        if passed == total:
            print(colorize(f"All {total} checks passed!", Colors.GREEN))
        else:
            print(colorize(f"{passed}/{total} checks passed", Colors.YELLOW if passed > total/2 else Colors.RED))

        return passed == total

def main():
    parser = argparse.ArgumentParser(
        description="Validate Claude Code skills against best practices"
    )
    parser.add_argument(
        "path",
        help="Path to skill directory or SKILL.md file"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    validator = SkillValidator(args.path)
    all_passed, results = validator.validate()

    if args.json:
        output = {
            "skill_path": str(validator.skill_path),
            "all_passed": all_passed,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details
                }
                for r in results
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        validator.print_results()

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
