import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class RepositoryContractTests(unittest.TestCase):
    def test_required_public_files_exist(self) -> None:
        required = {
            "SKILL.md",
            "agents/openai.yaml",
            "README.md",
            "README.zh-CN.md",
            "examples/complete-validation.md",
            "examples/insufficient-evidence.zh-CN.md",
            "evals/cases.json",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "LICENSE",
            "VERSION",
        }
        missing = sorted(path for path in required if not (ROOT / path).is_file())
        self.assertEqual(missing, [], f"Missing public files: {missing}")

    def test_skill_identity_and_discovery_metadata(self) -> None:
        skill = read("SKILL.md")
        frontmatter_match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
        self.assertIsNotNone(frontmatter_match, "SKILL.md needs YAML frontmatter")
        frontmatter = frontmatter_match.group(1)
        keys = [
            line.split(":", 1)[0].strip()
            for line in frontmatter.splitlines()
            if line.strip() and not line.startswith((" ", "\t"))
        ]
        self.assertEqual(keys, ["name", "description"])
        self.assertIn("name: solo-business-validation-skill", frontmatter)
        description = next(
            line.split(":", 1)[1].strip()
            for line in frontmatter.splitlines()
            if line.startswith("description:")
        )
        self.assertTrue(description.startswith("Use when"))
        for term in ("solo business", "side project", "AI product"):
            self.assertIn(term, description)

    def test_skill_preserves_evidence_states_and_business_dimensions(self) -> None:
        skill = read("SKILL.md")
        for term in (
            "Verified",
            "Early signal",
            "User statement",
            "External inference",
            "Unknown",
            "已核实",
            "初步信号",
            "用户陈述",
            "外部推断",
            "未知",
            "Demand",
            "Buyer",
            "Distribution",
            "Payment",
            "Delivery economics",
            "Compounding value",
            "Ceiling",
            "Risk",
        ):
            self.assertIn(term, skill)

    def test_skill_requires_decision_experiment_and_stop_conditions(self) -> None:
        skill = read("SKILL.md")
        for term in (
            "Decision",
            "One-sentence rationale",
            "Evidence ledger",
            "Business assessment",
            "Smallest decisive experiment",
            "Next three actions",
            "Pass line",
            "Stop line",
            "Time cap",
            "Money cap",
            "Human approval",
        ):
            self.assertIn(term, skill)
        self.assertRegex(skill, r"(?i)(do not|never).{0,80}(invent|unsupported).{0,80}score")

    def test_openai_metadata_names_the_public_skill(self) -> None:
        metadata = read("agents/openai.yaml")
        self.assertIn('$solo-business-validation-skill', metadata)
        self.assertIn('display_name: "Solo Business Validation"', metadata)

    def test_readmes_explain_audience_difference_and_compatibility(self) -> None:
        english = read("README.md")
        chinese = read("README.zh-CN.md")
        for term in ("solo founders", "missing evidence", "Codex", "Claude Code", "Agent Skills"):
            self.assertIn(term, english)
        for term in ("一人公司", "缺失证据", "Codex", "Claude Code", "Agent Skills"):
            self.assertIn(term, chinese)

    def test_examples_show_full_and_insufficient_evidence_paths(self) -> None:
        complete = read("examples/complete-validation.md")
        insufficient = read("examples/insufficient-evidence.zh-CN.md")
        for term in ("Verified", "Payment", "Pass line", "Stop line", "Money cap"):
            self.assertIn(term, complete)
        for term in ("用户陈述", "初步信号", "未知", "先补关键证据", "停止线"):
            self.assertIn(term, insufficient)

    def test_evals_cover_decisive_and_insufficient_evidence(self) -> None:
        cases = json.loads(read("evals/cases.json"))
        self.assertGreaterEqual(len(cases), 3)
        self.assertTrue(any(case["expected_decision"] == "expand_in_stages" for case in cases))
        self.assertTrue(any(case["expected_decision"] == "pause_or_research" for case in cases))
        for case in cases:
            self.assertIsInstance(case["prompt"], str)
            self.assertGreaterEqual(len(case["expected_behaviors"]), 4)

    def test_public_text_has_no_secrets_or_machine_specific_home_paths(self) -> None:
        windows_home = re.compile(r"[A-Za-z]:[/\\]" + r"Users[/\\][^/\\\s]+", re.IGNORECASE)
        unix_home = re.compile(r"/(?:Users|home)/[^/\s]+/")
        private_key = re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY")
        github_token = re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")
        ignored_parts = {".git", "work", "outputs", "dist", "__pycache__"}

        findings = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(part in ignored_parts for part in path.parts):
                continue
            if path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".py", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8")
            for label, pattern in (
                ("Windows home path", windows_home),
                ("Unix home path", unix_home),
                ("private key", private_key),
                ("GitHub token", github_token),
            ):
                if pattern.search(text):
                    findings.append(f"{path.relative_to(ROOT)}: {label}")

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
