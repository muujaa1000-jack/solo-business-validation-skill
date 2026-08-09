import hashlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_package_is_deterministic_minimal_and_verifiable(self) -> None:
        from scripts.package import build
        from scripts.verify_artifacts import verify

        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            first = build(ROOT, temp / "first")
            second = build(ROOT, temp / "second")

            first_zip, first_skill, first_sums = first
            second_zip, second_skill, second_sums = second

            self.assertEqual(first_zip.read_bytes(), second_zip.read_bytes())
            self.assertEqual(first_skill.read_bytes(), second_skill.read_bytes())
            self.assertEqual(first_sums.read_bytes(), second_sums.read_bytes())
            self.assertEqual(first_zip.read_bytes(), first_skill.read_bytes())

            version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
            self.assertEqual(first_zip.name, f"solo-business-validation-skill-{version}.zip")
            self.assertEqual(first_skill.name, f"solo-business-validation-skill-{version}.skill")
            self.assertEqual(first_sums.name, "SHA256SUMS")

            top = "solo-business-validation-skill"
            with zipfile.ZipFile(first_zip) as archive:
                self.assertEqual(
                    archive.namelist(),
                    [f"{top}/LICENSE", f"{top}/SKILL.md", f"{top}/agents/openai.yaml"],
                )

            self.assertEqual(verify(ROOT, first_zip), [])
            self.assertEqual(verify(ROOT, first_skill), [])

            digest = hashlib.sha256(first_zip.read_bytes()).hexdigest()
            sums = first_sums.read_text(encoding="utf-8")
            self.assertIn(f"{digest}  {first_zip.name}", sums)
            self.assertIn(f"{digest}  {first_skill.name}", sums)

    def test_verifier_rejects_path_traversal_and_extra_files(self) -> None:
        from scripts.verify_artifacts import verify

        with tempfile.TemporaryDirectory() as temporary:
            archive_path = Path(temporary) / "unsafe.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../escape.txt", "unsafe")

            findings = verify(ROOT, archive_path)
            self.assertTrue(any("unsafe archive path" in finding for finding in findings))
            self.assertTrue(any("archive members differ" in finding for finding in findings))

    def test_cli_reports_missing_artifacts_without_a_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/verify_artifacts.py"),
                    str(temp / "missing.zip"),
                    str(temp / "missing.skill"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("artifact does not exist", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
