#!/usr/bin/env python3
"""Verify Skill release archive structure, source hashes, and safety."""

from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path, PurePosixPath

try:
    from scripts.validate import RUNTIME_FILES, SKILL_NAME, scan_text
except ModuleNotFoundError:  # Direct execution from scripts/.
    from validate import RUNTIME_FILES, SKILL_NAME, scan_text


def expected_members() -> list[str]:
    return [f"{SKILL_NAME}/{Path(relative).as_posix()}" for relative in sorted(RUNTIME_FILES)]


def _unsafe(name: str) -> bool:
    path = PurePosixPath(name)
    return (
        not name
        or name.startswith(("/", "\\"))
        or "\\" in name
        or any(part in {"", ".", ".."} for part in path.parts)
    )


def verify(root: Path, artifact: Path) -> list[str]:
    root = root.resolve()
    artifact = artifact.resolve()
    findings: list[str] = []
    if not artifact.is_file():
        return [f"artifact does not exist: {artifact}"]

    try:
        with zipfile.ZipFile(artifact) as archive:
            members = archive.namelist()
            for name in members:
                if _unsafe(name):
                    findings.append(f"{artifact.name}: unsafe archive path: {name}")

            expected = expected_members()
            if members != expected:
                findings.append(
                    f"{artifact.name}: archive members differ; expected {expected}, got {members}"
                )

            for relative, member in zip(sorted(RUNTIME_FILES), expected):
                if member not in members:
                    continue
                payload = archive.read(member)
                source = (root / relative).read_bytes()
                if hashlib.sha256(payload).digest() != hashlib.sha256(source).digest():
                    findings.append(f"{artifact.name}: content hash differs for {relative}")
                try:
                    text = payload.decode("utf-8")
                except UnicodeDecodeError:
                    findings.append(f"{artifact.name}: {relative} is not valid UTF-8")
                else:
                    findings.extend(scan_text(f"{artifact.name}:{relative}", text))
    except (OSError, zipfile.BadZipFile) as error:
        findings.append(f"{artifact.name}: cannot read ZIP payload: {error}")
    return findings


def _verify_checksums(artifacts: list[Path]) -> list[str]:
    if not artifacts:
        return []
    sums_path = artifacts[0].parent / "SHA256SUMS"
    if not sums_path.is_file():
        return [f"missing checksum file: {sums_path}"]

    expected: dict[str, str] = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if "  " not in line:
            return [f"malformed checksum line: {line!r}"]
        digest, name = line.split("  ", 1)
        expected[name] = digest

    findings: list[str] = []
    for artifact in artifacts:
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        if expected.get(artifact.name) != digest:
            findings.append(f"checksum mismatch for {artifact.name}")
    return findings


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if not arguments:
        print("usage: verify_artifacts.py ARTIFACT [ARTIFACT ...]", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parents[1]
    artifacts = [Path(argument).resolve() for argument in arguments]
    findings: list[str] = []
    for artifact in artifacts:
        findings.extend(verify(root, artifact))
    if len(artifacts) >= 2 and artifacts[0].read_bytes() != artifacts[1].read_bytes():
        findings.append("ZIP and .skill payloads are not byte-identical")
    findings.extend(_verify_checksums(artifacts))

    if findings:
        for finding in findings:
            print(f"[ERROR] {finding}", file=sys.stderr)
        return 1
    for artifact in artifacts:
        print(f"[OK] verified {artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
