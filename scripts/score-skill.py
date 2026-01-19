#!/usr/bin/env python3
"""
Skill Quality Scorer - Rate Claude Code skills 0-100

Scoring breakdown (100 points total):
- Structure: 15 pts
- Description: 25 pts
- Content: 25 pts
- Progressive Disclosure: 15 pts
- Examples: 10 pts
- Cross-Platform: 10 pts
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# ANSI colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def colorize(text: str, color: str) -> str:
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.END}"
    return text

@dataclass
class ScoreCategory:
    """Score breakdown for a category."""
    name: str
    max_points: int
    earned_points: float
    breakdown: List[str]
    recommendations: List[str]

    @property
    def percentage(self) -> float:
        return (self.earned_points / self.max_points) * 100 if self.max_points > 0 else 0

class SkillScorer:
    """Score Claude Code skills on quality metrics."""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path).resolve()
        self.skill_md_path = None
        self.content = ""
        self.frontmatter = {}
        self.body = ""
        self.categories: List[ScoreCategory] = []

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

    def score_structure(self) -> ScoreCategory:
        """Score: Structure (15 points)"""
        points = 0.0
        breakdown = []
        recommendations = []

        # SKILL.md exists (5 points)
        if self.skill_md_path and self.skill_md_path.exists():
            points += 5
            breakdown.append("+5: SKILL.md exists")
        else:
            breakdown.append("+0: SKILL.md missing")
            recommendations.append("Create a SKILL.md file")

        # references/ directory (4 points)
        references_dir = self.skill_path / "references"
        if references_dir.exists() and any(references_dir.iterdir()):
            points += 4
            breakdown.append("+4: references/ directory with content")
        elif "references/" in self.content:
            points += 2
            breakdown.append("+2: references/ mentioned but directory missing")
            recommendations.append("Create references/ directory")
        else:
            breakdown.append("+0: No references/ structure")
            recommendations.append("Consider adding references/ for documentation")

        # scripts/ directory (4 points)
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists() and any(scripts_dir.iterdir()):
            # Check if scripts are executable
            all_executable = True
            for script in scripts_dir.glob('*'):
                if script.suffix in ['.sh', '.py'] and not os.access(script, os.X_OK):
                    all_executable = False

            if all_executable:
                points += 4
                breakdown.append("+4: scripts/ with executable files")
            else:
                points += 3
                breakdown.append("+3: scripts/ exists but some not executable")
                recommendations.append("Make scripts executable: chmod +x scripts/*")
        elif "scripts/" in self.content:
            points += 1
            breakdown.append("+1: scripts/ mentioned but directory missing")
            recommendations.append("Create scripts/ directory")
        else:
            breakdown.append("+0: No scripts/ (may not be needed)")

        # Clean directory structure (2 points)
        unwanted = ['.DS_Store', 'Thumbs.db', '__pycache__', '.pyc']
        has_unwanted = any((self.skill_path / u).exists() for u in unwanted)
        if not has_unwanted:
            points += 2
            breakdown.append("+2: Clean directory (no junk files)")
        else:
            breakdown.append("+0: Contains unwanted files")
            recommendations.append("Remove .DS_Store, __pycache__, etc.")

        return ScoreCategory("Structure", 15, points, breakdown, recommendations)

    def score_description(self) -> ScoreCategory:
        """Score: Description (25 points)"""
        points = 0.0
        breakdown = []
        recommendations = []

        description = self.frontmatter.get('description', '')

        # Has name field (3 points)
        name = self.frontmatter.get('name', '')
        if name and re.match(r'^[a-z0-9-]+$', name):
            points += 3
            breakdown.append("+3: Valid name field")
        elif name:
            points += 1
            breakdown.append("+1: Name field exists but format incorrect")
            recommendations.append("Use lowercase-with-dashes format for name")
        else:
            breakdown.append("+0: Missing name field")
            recommendations.append("Add 'name' to frontmatter")

        # Description length (5 points)
        desc_len = len(description)
        if desc_len >= 100:
            points += 5
            breakdown.append("+5: Description is comprehensive")
        elif desc_len >= 50:
            points += 3
            breakdown.append("+3: Description is adequate")
            recommendations.append("Expand description with more trigger phrases")
        elif desc_len >= 20:
            points += 1
            breakdown.append("+1: Description is minimal")
            recommendations.append("Add more detail and trigger phrases")
        else:
            breakdown.append("+0: Description too short")
            recommendations.append("Write comprehensive description (100+ chars)")

        # Trigger phrases (8 points)
        trigger_patterns = [
            r'[Tt]riggers?\s+for',
            r'[Aa]ctivates?\s+(?:for|when)',
            r'[Uu]se\s+when',
            r'"[^"]+",?\s*"[^"]+"',  # Quoted phrases
        ]
        trigger_count = sum(1 for p in trigger_patterns if re.search(p, description))

        if trigger_count >= 2:
            points += 8
            breakdown.append("+8: Multiple trigger patterns found")
        elif trigger_count == 1:
            points += 4
            breakdown.append("+4: One trigger pattern found")
            recommendations.append("Add more trigger phrases for better auto-detection")
        else:
            breakdown.append("+0: No trigger phrases")
            recommendations.append("Add 'Triggers for: \"phrase1\", \"phrase2\"'")

        # Specificity (5 points)
        specific_indicators = ['when', 'for', 'to', 'that', 'which']
        generic_words = ['help', 'assist', 'support', 'various', 'many', 'general']

        specific_count = sum(1 for w in specific_indicators if w in description.lower())
        generic_count = sum(1 for w in generic_words if w in description.lower())

        specificity_score = specific_count - generic_count

        if specificity_score >= 2:
            points += 5
            breakdown.append("+5: Description is specific")
        elif specificity_score >= 0:
            points += 3
            breakdown.append("+3: Description moderately specific")
            recommendations.append("Make description more specific")
        else:
            points += 1
            breakdown.append("+1: Description is too generic")
            recommendations.append("Avoid generic words like 'help', 'various'")

        # Context field if needed (4 points)
        has_context = 'context' in self.frontmatter
        is_conversational = any(word in self.body.lower() for word in ['you are', 'your role', 'persona'])

        if is_conversational and has_context:
            points += 4
            breakdown.append("+4: context:fork properly specified")
        elif is_conversational and not has_context:
            points += 1
            breakdown.append("+1: Conversational skill but missing context:fork")
            recommendations.append("Add 'context: fork' for conversational skills")
        elif not is_conversational:
            points += 4
            breakdown.append("+4: Non-conversational (context not required)")

        return ScoreCategory("Description", 25, points, breakdown, recommendations)

    def score_content(self) -> ScoreCategory:
        """Score: Content (25 points)"""
        points = 0.0
        breakdown = []
        recommendations = []

        # Headers/structure (6 points)
        h1_count = len(re.findall(r'^#\s', self.body, re.MULTILINE))
        h2_count = len(re.findall(r'^##\s', self.body, re.MULTILINE))
        h3_count = len(re.findall(r'^###\s', self.body, re.MULTILINE))

        total_headers = h1_count + h2_count + h3_count

        if h1_count == 1 and h2_count >= 3:
            points += 6
            breakdown.append("+6: Well-structured with proper header hierarchy")
        elif total_headers >= 4:
            points += 4
            breakdown.append("+4: Good header structure")
        elif total_headers >= 2:
            points += 2
            breakdown.append("+2: Basic structure")
            recommendations.append("Add more section headers")
        else:
            breakdown.append("+0: Poor structure")
            recommendations.append("Add section headers (##, ###)")

        # Code blocks (6 points)
        code_blocks = re.findall(r'```(\w*)\n[\s\S]*?```', self.body)

        if len(code_blocks) >= 4:
            points += 6
            breakdown.append("+6: Excellent code examples")
        elif len(code_blocks) >= 2:
            points += 4
            breakdown.append("+4: Good code examples")
        elif len(code_blocks) >= 1:
            points += 2
            breakdown.append("+2: Some code examples")
            recommendations.append("Add more code examples")
        else:
            breakdown.append("+0: No code examples")
            recommendations.append("Add code examples with ```language blocks")

        # Imperative form (5 points)
        passive_patterns = ['you should', 'you can', 'you will', 'you may', 'you need to']
        imperative_patterns = ['run', 'create', 'add', 'use', 'check', 'verify', 'ensure']

        passive_count = sum(len(re.findall(p, self.body.lower())) for p in passive_patterns)
        imperative_count = sum(len(re.findall(rf'\b{p}\b', self.body.lower())) for p in imperative_patterns)

        ratio = imperative_count / (passive_count + 1)

        if ratio >= 3:
            points += 5
            breakdown.append("+5: Strong imperative form")
        elif ratio >= 1.5:
            points += 3
            breakdown.append("+3: Good imperative form")
            recommendations.append("Reduce passive voice")
        elif ratio >= 0.5:
            points += 1
            breakdown.append("+1: Too much passive voice")
            recommendations.append("Use imperative: 'Run tests' not 'You should run tests'")
        else:
            breakdown.append("+0: Mostly passive voice")
            recommendations.append("Rewrite in imperative form")

        # Tables for organization (4 points)
        table_count = len(re.findall(r'^\|.*\|$', self.body, re.MULTILINE))

        if table_count >= 6:
            points += 4
            breakdown.append("+4: Good use of tables")
        elif table_count >= 2:
            points += 2
            breakdown.append("+2: Some table usage")
        else:
            breakdown.append("+0: No tables")
            recommendations.append("Consider adding tables for structured info")

        # Lists for steps (4 points)
        bullet_count = len(re.findall(r'^[-*]\s', self.body, re.MULTILINE))
        numbered_count = len(re.findall(r'^\d+\.\s', self.body, re.MULTILINE))

        list_count = bullet_count + numbered_count

        if list_count >= 8:
            points += 4
            breakdown.append("+4: Good use of lists")
        elif list_count >= 4:
            points += 2
            breakdown.append("+2: Some list usage")
        else:
            breakdown.append("+0: Few lists")
            recommendations.append("Use lists for steps and options")

        return ScoreCategory("Content", 25, points, breakdown, recommendations)

    def score_progressive_disclosure(self) -> ScoreCategory:
        """Score: Progressive Disclosure (15 points)"""
        points = 0.0
        breakdown = []
        recommendations = []

        line_count = len(self.content.split('\n'))

        # Main file length (8 points)
        if line_count <= 200:
            points += 8
            breakdown.append("+8: Concise main file (<200 lines)")
        elif line_count <= 350:
            points += 6
            breakdown.append("+6: Good main file length (<350 lines)")
        elif line_count <= 500:
            points += 4
            breakdown.append("+4: Acceptable length (<500 lines)")
        elif line_count <= 700:
            points += 2
            breakdown.append("+2: Main file is long")
            recommendations.append("Move content to references/")
        else:
            breakdown.append(f"+0: Main file too long ({line_count} lines)")
            recommendations.append("Significantly reduce SKILL.md size")

        # References usage (5 points)
        references_dir = self.skill_path / "references"
        ref_mentions = len(re.findall(r'references/', self.content))

        if references_dir.exists():
            ref_files = list(references_dir.glob('*.md'))
            if len(ref_files) >= 2 and ref_mentions >= 2:
                points += 5
                breakdown.append("+5: Good use of references/")
            elif len(ref_files) >= 1:
                points += 3
                breakdown.append("+3: Some use of references/")
            else:
                points += 1
                breakdown.append("+1: references/ exists but empty")
                recommendations.append("Add documentation to references/")
        elif line_count > 300:
            breakdown.append("+0: Long file without references/")
            recommendations.append("Create references/ folder for details")
        else:
            points += 3
            breakdown.append("+3: Short file (references not required)")

        # No duplicate content (2 points)
        # Simple check: look for repeated paragraphs
        paragraphs = [p.strip() for p in self.body.split('\n\n') if len(p.strip()) > 50]
        unique_paragraphs = set(paragraphs)

        if len(paragraphs) == len(unique_paragraphs):
            points += 2
            breakdown.append("+2: No duplicate content")
        else:
            breakdown.append("+0: Some duplicate content")
            recommendations.append("Remove duplicate paragraphs")

        return ScoreCategory("Progressive Disclosure", 15, points, breakdown, recommendations)

    def score_examples(self) -> ScoreCategory:
        """Score: Examples (10 points)"""
        points = 0.0
        breakdown = []
        recommendations = []

        # Count example sections
        example_headers = len(re.findall(r'^#{1,3}\s*[Ee]xample', self.body, re.MULTILINE))
        example_mentions = len(re.findall(r'\b[Ee]xample\s*\d*:', self.body))

        total_examples = example_headers + example_mentions

        # Number of examples (5 points)
        if total_examples >= 3:
            points += 5
            breakdown.append("+5: Multiple examples provided")
        elif total_examples >= 1:
            points += 3
            breakdown.append("+3: Some examples")
            recommendations.append("Add more examples (aim for 3+)")
        else:
            breakdown.append("+0: No examples")
            recommendations.append("Add example sections")

        # Examples with expected output (3 points)
        output_patterns = ['output', 'result', 'returns', 'produces', 'expected']
        examples_with_output = sum(1 for p in output_patterns if p in self.body.lower())

        if examples_with_output >= 2:
            points += 3
            breakdown.append("+3: Examples show expected outputs")
        elif examples_with_output >= 1:
            points += 1
            breakdown.append("+1: Some examples show output")
            recommendations.append("Add expected outputs to examples")
        else:
            breakdown.append("+0: Examples don't show outputs")
            recommendations.append("Show expected output for each example")

        # Realistic examples (2 points)
        placeholder_patterns = ['foo', 'bar', 'baz', 'xxx', 'example.com', 'lorem']
        placeholder_count = sum(len(re.findall(p, self.body.lower())) for p in placeholder_patterns)

        if placeholder_count <= 1:
            points += 2
            breakdown.append("+2: Realistic examples")
        elif placeholder_count <= 3:
            points += 1
            breakdown.append("+1: Some placeholder text in examples")
            recommendations.append("Use realistic values instead of foo/bar")
        else:
            breakdown.append("+0: Too many placeholders")
            recommendations.append("Replace foo/bar/example.com with realistic values")

        return ScoreCategory("Examples", 10, points, breakdown, recommendations)

    def score_cross_platform(self) -> ScoreCategory:
        """Score: Cross-Platform (10 points)"""
        points = 0.0
        breakdown = []
        recommendations = []

        # agentskills.io fields (5 points)
        agentskills_fields = {
            'version': 1,
            'platforms': 1.5,
            'inputs': 1,
            'outputs': 1,
            'tags': 0.5,
        }

        field_points = 0
        for field, pts in agentskills_fields.items():
            if field in self.frontmatter:
                field_points += pts

        if field_points >= 4:
            points += 5
            breakdown.append("+5: Full agentskills.io compliance")
        elif field_points >= 2:
            points += field_points
            breakdown.append(f"+{field_points}: Partial agentskills.io fields")
            recommendations.append("Add more agentskills.io fields")
        else:
            breakdown.append("+0: No agentskills.io fields")
            recommendations.append("Consider adding: version, platforms, tags")

        # manifest.json (3 points)
        manifest_path = self.skill_path / "manifest.json"
        if manifest_path.exists():
            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)
                if 'name' in manifest and 'description' in manifest:
                    points += 3
                    breakdown.append("+3: Valid manifest.json")
                else:
                    points += 1
                    breakdown.append("+1: manifest.json incomplete")
                    recommendations.append("Add required fields to manifest.json")
            except json.JSONDecodeError:
                breakdown.append("+0: Invalid manifest.json")
                recommendations.append("Fix manifest.json syntax")
        else:
            breakdown.append("+0: No manifest.json")
            recommendations.append("Add manifest.json for registry listing")

        # Platform-agnostic content (2 points)
        claude_specific = ['claude code', 'claude-code', 'anthropic']
        specific_count = sum(len(re.findall(p, self.body.lower())) for p in claude_specific)

        if specific_count <= 2:
            points += 2
            breakdown.append("+2: Platform-agnostic content")
        elif specific_count <= 5:
            points += 1
            breakdown.append("+1: Some Claude-specific references")
            recommendations.append("Use platform-neutral language where possible")
        else:
            breakdown.append("+0: Heavy Claude-specific content")
            recommendations.append("Make content more platform-agnostic")

        return ScoreCategory("Cross-Platform", 10, points, breakdown, recommendations)

    def calculate_score(self) -> Tuple[float, List[ScoreCategory]]:
        """Calculate total score."""
        if not self.find_skill_file():
            return 0, []

        if not self.parse_frontmatter():
            return 0, []

        self.categories = [
            self.score_structure(),
            self.score_description(),
            self.score_content(),
            self.score_progressive_disclosure(),
            self.score_examples(),
            self.score_cross_platform(),
        ]

        total = sum(c.earned_points for c in self.categories)
        return total, self.categories

    def get_grade(self, score: float) -> Tuple[str, str]:
        """Get letter grade and color."""
        if score >= 90:
            return 'A', Colors.GREEN
        elif score >= 80:
            return 'B', Colors.GREEN
        elif score >= 70:
            return 'C', Colors.YELLOW
        elif score >= 60:
            return 'D', Colors.YELLOW
        else:
            return 'F', Colors.RED

    def print_results(self):
        """Print scoring results."""
        score, categories = self.calculate_score()

        if not categories:
            print(colorize("Error: Could not analyze skill", Colors.RED))
            return False

        grade, grade_color = self.get_grade(score)

        print(colorize("\n=== Skill Quality Score ===\n", Colors.BOLD))
        print(f"Skill: {self.skill_path.name}")
        print(f"Path: {self.skill_path}\n")

        # Score bar
        bar_width = 40
        filled = int((score / 100) * bar_width)
        bar = '█' * filled + '░' * (bar_width - filled)

        print(f"Score: {colorize(f'{score:.1f}/100', grade_color)} [{bar}]")
        print(f"Grade: {colorize(grade, grade_color)}\n")

        # Category breakdown
        print(colorize("Category Breakdown:", Colors.BOLD))
        print("-" * 60)

        for cat in categories:
            cat_bar_width = 20
            cat_filled = int((cat.percentage / 100) * cat_bar_width)
            cat_bar = '█' * cat_filled + '░' * (cat_bar_width - cat_filled)

            print(f"\n{colorize(cat.name, Colors.CYAN)} ({cat.earned_points:.1f}/{cat.max_points})")
            print(f"  [{cat_bar}] {cat.percentage:.0f}%")

            for item in cat.breakdown:
                print(f"    {item}")

        # Top recommendations
        all_recs = []
        for cat in categories:
            all_recs.extend(cat.recommendations)

        if all_recs:
            print(colorize("\nTop Recommendations:", Colors.BOLD))
            for rec in all_recs[:5]:
                print(f"  • {rec}")

        print()

        if score >= 80:
            print(colorize("This skill meets quality standards!", Colors.GREEN))
        elif score >= 60:
            print(colorize("This skill needs some improvements.", Colors.YELLOW))
        else:
            print(colorize("This skill needs significant work.", Colors.RED))

        return score >= 80

def main():
    parser = argparse.ArgumentParser(
        description="Score Claude Code skill quality (0-100)"
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
    parser.add_argument(
        "--min-score",
        type=float,
        default=0,
        help="Exit with error if score is below this value"
    )

    args = parser.parse_args()

    scorer = SkillScorer(args.path)
    score, categories = scorer.calculate_score()

    if args.json:
        output = {
            "skill_path": str(scorer.skill_path),
            "score": round(score, 1),
            "grade": scorer.get_grade(score)[0],
            "categories": [
                {
                    "name": c.name,
                    "earned": c.earned_points,
                    "max": c.max_points,
                    "percentage": round(c.percentage, 1),
                    "breakdown": c.breakdown,
                    "recommendations": c.recommendations
                }
                for c in categories
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        scorer.print_results()

    if args.min_score and score < args.min_score:
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
