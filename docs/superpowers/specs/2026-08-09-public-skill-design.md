# Public Skill Design

## Goal

Publish `solo-business-validation-skill` as a small, trustworthy Agent Skill for solo founders, indie hackers, side projects, AI products, and other one-person businesses. It should help a stranger decide whether to build, continue, expand, pause, or stop based on evidence instead of enthusiasm or invented scores.

## Product boundary

The repository root is the installable Skill. The first release keeps one Skill rather than becoming a general startup-advice toolkit.

The Skill must:

- classify evidence as verified, early signal, user statement, external inference, or unknown;
- treat missing evidence as unknown rather than zero;
- assess demand, buyer, distribution, payment, delivery economics, compounding value, ceiling, and risk;
- design the smallest decisive experiment with pass and stop lines plus time and money caps;
- keep spending and other irreversible actions behind human approval;
- refuse unsupported precise scores and avoid treating likes, friendly praise, market growth, or an existing prototype as proof.

## Repository shape

- `SKILL.md` and `agents/openai.yaml`: the installable Skill.
- `README.md` and `README.zh-CN.md`: English and Chinese entry points, compatibility, installation, and differentiation.
- `examples/`: one complete validation and one insufficient-evidence stop-or-research case.
- `tests/`: lightweight contract tests for metadata, evidence rules, output structure, examples, public-safety requirements, and distribution contents.
- `scripts/`: cross-platform validation and packaging helpers with no machine-specific paths.
- `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, and `SECURITY.md`: minimum maintenance and release foundations.
- GitHub Actions: run contract tests, the official quick validator, public-safety checks, and package verification on supported pushes and pull requests.

## Distribution

Version `0.1.0` is the first public release. The build produces both a conventional ZIP archive and the same ZIP-compatible artifact with a `.skill` extension. Each archive contains one top-level `solo-business-validation-skill/` directory and only runtime files needed to install the Skill.

A tagged GitHub release attaches both artifacts and checksums. Packaging is reproducible from a clean checkout, and unpacked artifacts must pass the same Skill and privacy validation as the source.

## Compatibility

The core format follows the Agent Skills convention: a directory with a YAML-frontmatter `SKILL.md`, plus optional agent metadata. Documentation will distinguish tested local validation from general directory-format compatibility. It will not claim verified support for a host unless that host's current official installation model was checked.

## Safety and privacy

Public files and Git history must not include credentials, private business records, store or customer identifiers, real product details, or local absolute paths. Examples use clearly fictional or composite businesses. Automated checks cover common credentials, Windows user paths, private keys, and known private terms, while final review also inspects tracked files and release archives.

## Verification

Completion requires:

1. contract tests passing in UTF-8 mode;
2. official Skill validation passing for the source directory;
3. both release artifacts unpacking and passing the same validation;
4. artifact runtime files matching the source by SHA-256;
5. public-safety scans passing for tracked files, Git history, and unpacked artifacts;
6. the public GitHub repository, metadata, topics, default branch, tag, and release being readable after push.

## Non-goals for v0.1.0

- No hosted service, telemetry, external API, database, or production dependency.
- No generalized market-research engine or automatic financial forecast.
- No private operating examples or platform-specific business advice.
- No promise that one validation result replaces founder judgment or professional legal, financial, or regulatory advice.
