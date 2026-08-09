#!/usr/bin/env python3
"""Build deterministic ZIP-compatible Skill release artifacts."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

try:
    from scripts.validate import RUNTIME_FILES, SKILL_NAME, validate_repository
except ModuleNotFoundError:  # Direct execution from scripts/.
    from validate import RUNTIME_FILES, SKILL_NAME, validate_repository


FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def build(root: Path, output_dir: Path) -> tuple[Path, Path, Path]:
    root = root.resolve()
    output_dir = output_dir.resolve()
    findings = validate_repository(root)
    if findings:
        formatted = "\n".join(f"- {finding}" for finding in findings)
        raise ValueError(f"repository validation failed:\n{formatted}")

    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / f"{SKILL_NAME}-{version}.zip"
    skill_path = output_dir / f"{SKILL_NAME}-{version}.skill"
    sums_path = output_dir / "SHA256SUMS"

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in sorted(RUNTIME_FILES):
            archive_name = f"{SKILL_NAME}/{Path(relative).as_posix()}"
            archive.writestr(_zip_info(archive_name), (root / relative).read_bytes())

    shutil.copyfile(zip_path, skill_path)
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    sums = f"{digest}  {zip_path.name}\n{digest}  {skill_path.name}\n"
    sums_path.write_text(sums, encoding="utf-8", newline="\n")
    return zip_path, skill_path, sums_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        artifacts = build(root, args.output_dir)
    except ValueError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 1
    for artifact in artifacts:
        print(f"[OK] wrote {artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
