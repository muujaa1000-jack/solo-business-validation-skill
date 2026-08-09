#!/usr/bin/env python3
"""Validate repository contracts and public-safety boundaries."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable


SKILL_NAME = "solo-business-validation-skill"
RUNTIME_FILES = ("LICENSE", "SKILL.md", "agents/openai.yaml")
REQUIRED_FILES = (
    *RUNTIME_FILES,
    "README.md",
    "README.zh-CN.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "VERSION",
    "evals/cases.json",
    "examples/complete-validation.md",
    "examples/insufficient-evidence.zh-CN.md",
)
IGNORED_PARTS = {".git", "work", "outputs", "dist", "__pycache__", ".venv", "venv"}
TEXT_SUFFIXES = {"", ".md", ".yaml", ".yml", ".json", ".py", ".txt"}

WINDOWS_HOME = re.compile(r"[A-Za-z]:[/\\]Users[/\\][^/\\\s]+", re.IGNORECASE)
UNIX_HOME = re.compile(r"/(?:Users|home)/[^/\s]+/")
PRIVATE_KEY = re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY")
GITHUB_TOKEN = re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")
GENERIC_SECRET = re.compile(
    r"(?i)(?:api[_-]?key|secret|password|access[_-]?token)\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"
)
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\Z")


def iter_public_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def scan_text(label: str, text: str) -> list[str]:
    findings: list[str] = []
    for finding, pattern in (
        ("machine-specific Windows home path", WINDOWS_HOME),
        ("machine-specific Unix home path", UNIX_HOME),
        ("private key material", PRIVATE_KEY),
        ("GitHub access token", GITHUB_TOKEN),
        ("probable embedded secret", GENERIC_SECRET),
    ):
        if pattern.search(text):
            findings.append(f"{label}: {finding}")
    return findings


def parse_frontmatter(skill_text: str) -> tuple[list[str], dict[str, str]]:
    match = re.match(r"\A---\n(.*?)\n---\n", skill_text, re.DOTALL)
    if not match:
        return [], {}

    keys: list[str] = []
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        keys.append(key)
        values[key] = value.strip().strip("'\"")
    return keys, values


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    findings: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            findings.append(f"missing required file: {relative}")

    version_path = root / "VERSION"
    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        if not SEMVER.fullmatch(version):
            findings.append(f"VERSION is not stable semantic versioning: {version!r}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        keys, values = parse_frontmatter(skill)
        if keys != ["name", "description"]:
            findings.append(f"SKILL.md frontmatter keys must be name, description: {keys}")
        if values.get("name") != SKILL_NAME:
            findings.append(f"SKILL.md name must be {SKILL_NAME}")
        description = values.get("description", "")
        if not description.startswith("Use when"):
            findings.append("SKILL.md description must start with 'Use when'")
        if len(description) > 1024:
            findings.append("SKILL.md description exceeds 1024 characters")
        if len(skill.splitlines()) > 500:
            findings.append("SKILL.md exceeds 500 lines")

    metadata_path = root / "agents/openai.yaml"
    if metadata_path.is_file():
        metadata = metadata_path.read_text(encoding="utf-8")
        if f"${SKILL_NAME}" not in metadata:
            findings.append("agents/openai.yaml default prompt does not name the Skill")

    eval_path = root / "evals/cases.json"
    if eval_path.is_file():
        try:
            cases = json.loads(eval_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            findings.append(f"evals/cases.json is invalid JSON: {error}")
        else:
            if not isinstance(cases, list) or len(cases) < 3:
                findings.append("evals/cases.json must contain at least three cases")
            else:
                for index, case in enumerate(cases):
                    required = {"id", "prompt", "expected_decision", "expected_behaviors"}
                    if not isinstance(case, dict) or not required.issubset(case):
                        findings.append(f"eval case {index} lacks required fields")

    readme_path = root / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        for url in (
            "https://developers.openai.com/codex/skills",
            "https://code.claude.com/docs/en/skills",
            "https://agentskills.io/specification",
        ):
            if url not in readme:
                findings.append(f"README.md lacks official compatibility link: {url}")

    for path in iter_public_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"{path.relative_to(root).as_posix()}: not valid UTF-8 text")
            continue
        findings.extend(scan_text(path.relative_to(root).as_posix(), text))

    return findings


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    findings = validate_repository(root)
    if findings:
        for finding in findings:
            print(f"[ERROR] {finding}", file=sys.stderr)
        return 1
    print("[OK] repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
