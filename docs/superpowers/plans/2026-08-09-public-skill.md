# Public Solo Business Validation Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish version `0.1.0` of `solo-business-validation-skill` as a privacy-safe, bilingual, tested, and reproducibly packaged public Agent Skill.

**Architecture:** Keep the repository root compatible with the Agent Skills directory format while separating runtime files from contributor documentation and build tooling through an explicit package manifest. Use Python's standard library for contract tests, safety checks, deterministic packaging, and artifact verification; use GitHub Actions for continuous validation and tagged releases.

**Tech Stack:** Markdown, YAML, Python 3.10+ standard library, `unittest`, GitHub Actions, GitHub CLI.

## Global Constraints

- Version the first public release as `0.1.0`.
- Do not modify the installed private baseline; copy it only after the public contract tests fail as expected.
- Keep `SKILL.md` under 500 lines and use only forward-slash relative paths.
- Require no runtime package, external API, account, network access, or production dependency.
- Keep credentials, private business records, store or customer identifiers, real product details, and local absolute paths out of public files, Git history, and release artifacts.
- Treat missing evidence as unknown and never invent a precise score without a user-supplied complete rubric.
- Require a smallest decisive experiment with pass line, stop line, time cap, money cap, and human approval for spending or irreversible actions.
- Package only `SKILL.md`, `agents/openai.yaml`, and `LICENSE` under one top-level `solo-business-validation-skill/` directory.

## File Map

- `SKILL.md`: concise, host-neutral Agent Skill instructions and output contract.
- `agents/openai.yaml`: OpenAI/Codex display metadata and invocation prompt.
- `README.md`, `README.zh-CN.md`: English and Chinese public entry points, installation, compatibility, and differentiation.
- `examples/complete-validation.md`: full English example with mixed evidence and a staged expansion decision.
- `examples/insufficient-evidence.zh-CN.md`: Chinese stop-or-research example where praise and a prototype are insufficient.
- `evals/cases.json`: machine-readable evaluation prompts and expected behaviors.
- `evals/README.md`: model-evaluation procedure and reporting boundaries.
- `scripts/validate.py`: repository contracts and privacy checks using only the standard library.
- `scripts/package.py`: deterministic ZIP and `.skill` artifact builder plus checksums.
- `scripts/verify_artifacts.py`: archive structure, content hash, and privacy verifier.
- `tests/test_repository_contract.py`: public content and Skill behavior contracts.
- `tests/test_packaging.py`: deterministic package and archive-verification tests.
- `.github/workflows/ci.yml`: tests, validation, build, and artifact verification for pushes and pull requests.
- `.github/workflows/release.yml`: tagged release build and GitHub Release upload.
- `VERSION`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `.gitignore`, `.gitattributes`: release and maintenance foundation.

---

### Task 1: Define the public contracts and evaluations

**Files:**
- Create: `tests/test_repository_contract.py`
- Create: `evals/cases.json`
- Create: `evals/README.md`

**Interfaces:**
- Consumes: the product boundary in `docs/superpowers/specs/2026-08-09-public-skill-design.md`.
- Produces: `python -m unittest discover -s tests -p "test_*.py"`, which later tasks must keep green.

- [ ] **Step 1: Write failing repository-contract tests**

Create tests that require the public Skill name, only `name` and `description` frontmatter fields, the five evidence states in English and Chinese, all eight business dimensions, score refusal, the six semantic output sections, pass/stop/time/money limits, human approval, both README files, two examples, at least three eval cases, and no forbidden private markers or absolute user paths.

```python
class RepositoryContractTests(unittest.TestCase):
    def test_skill_identity_and_behavior(self):
        skill = read("SKILL.md")
        self.assertIn("name: solo-business-validation-skill", skill)
        for required in REQUIRED_BEHAVIOR:
            self.assertIn(required, skill)

    def test_evals_cover_decisive_and_insufficient_evidence(self):
        cases = json.loads(read("evals/cases.json"))
        self.assertGreaterEqual(len(cases), 3)
        self.assertTrue(any(case["expected_decision"] == "pause_or_research" for case in cases))
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `python -m unittest discover -s tests -p "test_*.py" -v`

Expected: FAIL because `SKILL.md`, public documentation, examples, and eval files do not exist yet.

- [ ] **Step 3: Add evaluation fixtures, not implementation guidance**

Define at least four fictional/composite scenarios in `evals/cases.json`: paid pilot with repeat use, friend praise plus prototype under sunk-cost pressure, macro-growth/content-like signals without payment, and an immediate-answer request with missing evidence. Each case records `prompt`, `expected_decision`, and an array of observable `expected_behaviors`.

- [ ] **Step 4: Commit the RED contract**

```bash
git add tests/test_repository_contract.py evals/
git commit -m "test: define public skill contracts"
```

### Task 2: Implement the runtime Skill

**Files:**
- Create: `SKILL.md`
- Create: `agents/openai.yaml`
- Create: `VERSION`

**Interfaces:**
- Consumes: the read-only installed baseline and Task 1 contracts.
- Produces: `$solo-business-validation-skill`, a host-neutral instruction-only Skill with OpenAI metadata.

- [ ] **Step 1: Copy the baseline into the repository**

Copy only the baseline `SKILL.md` and `agents/openai.yaml`; do not edit the installed source.

- [ ] **Step 2: Make the smallest public adaptation**

Set the frontmatter name to `solo-business-validation-skill`; front-load discovery terms in the description; instruct the agent to answer in the user's language; keep the five evidence states semantically exact; assess demand, buyer, distribution, payment, delivery economics, compounding value, ceiling, and risk; and render the six semantic sections in the user's language.

Use this decision set:

```text
continue_small_validation
gather_critical_evidence
pause_investment
expand_in_stages
```

Require the evidence ledger to show source and missing evidence. Require the experiment to contain hypothesis, payer profile, minimum deliverable, reachable channel, costly behavior, pass line, stop line, time cap, money cap, and approval gate.

- [ ] **Step 3: Regenerate and validate OpenAI metadata**

Use display name `Solo Business Validation`, a 25–64 character short description, and a one-sentence default prompt that explicitly includes `$solo-business-validation-skill`. Keep all YAML strings quoted.

- [ ] **Step 4: Run the contract and official Skill validators**

Run:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python -X utf8 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
```

Expected: contract tests remain RED only for documentation not yet added; the official validator prints `Skill is valid!`.

- [ ] **Step 5: Commit the runtime Skill**

```bash
git add SKILL.md agents/openai.yaml VERSION
git commit -m "feat: publish evidence-first validation skill"
```

### Task 3: Add public documentation and examples

**Files:**
- Create: `README.md`
- Create: `README.zh-CN.md`
- Create: `examples/complete-validation.md`
- Create: `examples/insufficient-evidence.zh-CN.md`
- Create: `CHANGELOG.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `LICENSE`
- Create: `.gitignore`
- Create: `.gitattributes`

**Interfaces:**
- Consumes: the exact behavior and invocation name from Task 2.
- Produces: stranger-friendly onboarding and two inspectable behavior examples without private data.

- [ ] **Step 1: Write both README entry points**

Put audience, problem, and differentiation in the first screen. Document three installation modes with current official links: Codex user skills under `$HOME/.agents/skills`, Claude Code personal skills under `~/.claude/skills`, and a host-selected Agent Skills directory. Explain that `agents/openai.yaml` is optional host metadata and `.skill` is a ZIP-compatible convenience artifact, not part of the base format specification.

- [ ] **Step 2: Write two complete fictional examples**

The English example must show verified paid-pilot and repeat-use evidence while limiting approval to a staged next test. The Chinese example must classify friends' praise, an existing prototype, and macro growth as non-payment evidence and conclude `先补关键证据` or `暂停投入` with a bounded experiment.

- [ ] **Step 3: Add maintenance files**

Use MIT license terms, Keep a Changelog headings, SemVer release rules, a pull-request checklist, a private-reporting security policy, LF normalization, and ignores for `dist/`, caches, virtual environments, and editor files.

- [ ] **Step 4: Run contracts and privacy searches**

Run:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
git grep -n -I -E "(BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|C:\\Users\\|/Users/[^/]+/)"
```

Expected: all tests PASS; the privacy search returns no match.

- [ ] **Step 5: Commit public documentation**

```bash
git add README.md README.zh-CN.md examples/ evals/ CHANGELOG.md CONTRIBUTING.md SECURITY.md LICENSE .gitignore .gitattributes
git commit -m "docs: add bilingual usage and maintenance guides"
```

### Task 4: Build deterministic validation and distribution

**Files:**
- Create: `tests/test_packaging.py`
- Create: `scripts/validate.py`
- Create: `scripts/package.py`
- Create: `scripts/verify_artifacts.py`

**Interfaces:**
- Produces: `scripts.validate.validate_repository(root: Path) -> list[str]`.
- Produces: `scripts.package.build(root: Path, output_dir: Path) -> tuple[Path, Path, Path]`.
- Produces: `scripts.verify_artifacts.verify(root: Path, artifact: Path) -> list[str]`.

- [ ] **Step 1: Write failing package tests**

```python
def test_package_is_deterministic_and_minimal(self):
    first = build(ROOT, self.output / "first")
    second = build(ROOT, self.output / "second")
    self.assertEqual(first[0].read_bytes(), second[0].read_bytes())
    self.assertEqual(first[1].read_bytes(), second[1].read_bytes())
    self.assertEqual(verify(ROOT, first[0]), [])
```

- [ ] **Step 2: Run the package test and verify RED**

Run: `python -m unittest tests.test_packaging -v`

Expected: ERROR because `scripts.package` and `scripts.verify_artifacts` do not exist.

- [ ] **Step 3: Implement repository validation**

Use standard-library parsing and regular expressions. Return every failure rather than stopping at the first. Validate required files, exact frontmatter keys, version format, README links, eval count, package manifest, local paths, private-key markers, token patterns, and forbidden private terms.

- [ ] **Step 4: Implement deterministic packaging**

Write fixed ZIP timestamps, sorted entries, normalized forward-slash names, and stable permissions. Emit:

```text
dist/solo-business-validation-skill-0.1.0.zip
dist/solo-business-validation-skill-0.1.0.skill
dist/SHA256SUMS
```

The ZIP and `.skill` payloads must be byte-identical.

- [ ] **Step 5: Implement archive verification**

Reject extra or missing members, path traversal, wrong top-level directories, mismatched source hashes, non-identical `.skill`/ZIP payloads, and public-safety findings.

- [ ] **Step 6: Run tests, build, and verify GREEN**

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate.py
python scripts/package.py
python scripts/verify_artifacts.py dist/solo-business-validation-skill-0.1.0.zip dist/solo-business-validation-skill-0.1.0.skill
```

Expected: all commands exit 0 and report no findings.

- [ ] **Step 7: Commit deterministic tooling**

```bash
git add scripts/ tests/test_packaging.py
git commit -m "build: add reproducible skill packages"
```

### Task 5: Add continuous integration and release automation

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/release.yml`

**Interfaces:**
- Consumes: the commands from Task 4.
- Produces: validated CI runs and release assets for tags matching `v*`.

- [ ] **Step 1: Add CI workflow**

Use `actions/checkout@v4` and `actions/setup-python@v5` with Python 3.10, 3.12, and 3.14. Run unit tests and `scripts/validate.py`; package and verify on Python 3.12; upload artifacts only from the packaging job.

- [ ] **Step 2: Add release workflow**

Trigger on `v*` tags, grant `contents: write`, rerun the full verification, and create or update the GitHub Release with ZIP, `.skill`, and checksum files through the authenticated GitHub CLI.

- [ ] **Step 3: Validate workflow syntax and commands locally**

Run all commands embedded in the workflows and inspect YAML indentation. Expected: every local command exits 0; workflow files contain no secrets or local paths.

- [ ] **Step 4: Commit automation**

```bash
git add .github/workflows/
git commit -m "ci: verify and release skill packages"
```

### Task 6: Verify, publish, and audit the public release

**Files:**
- Modify only if verification finds a defect.

**Interfaces:**
- Produces: public repository `muujaa1000-jack/solo-business-validation-skill`, tag `v0.1.0`, and release assets.

- [ ] **Step 1: Run the final local verification from a clean state**

Run unit tests, repository validation, official `quick_validate.py` with UTF-8 enabled, deterministic packaging, archive verification, `git diff --check`, tracked-file privacy scans, and a Git-history scan. Unpack both artifacts into fresh temporary directories and run the official validator against each top-level Skill directory.

- [ ] **Step 2: Review tracked content and release hashes**

Confirm `git status --short` is empty, the installed private baseline remains unchanged, the ZIP and `.skill` SHA-256 values match, and the three runtime file hashes match the source.

- [ ] **Step 3: Create and configure the public repository**

Create `muujaa1000-jack/solo-business-validation-skill` with public visibility, description, issues enabled, homepage pointing to the repository, and topics for Agent Skills, Codex, Claude Code, solo business, indie hackers, idea validation, and AI agents.

- [ ] **Step 4: Push main and publish v0.1.0**

Push `main`, create annotated tag `v0.1.0`, push the tag, wait for GitHub Actions, and repair any failure before continuing.

- [ ] **Step 5: Verify the public surface**

Read the remote repository, default branch, topics, workflow results, tag, release page, asset names, sizes, and published checksums through unauthenticated URLs where possible. Confirm no private data or local paths appear in the public Git history.

- [ ] **Step 6: Record final evidence**

Report the repository URL, exact checks run, any intentionally unverified model-behavior matrix, and the maintenance flow: edit → test → validate → package → tag → release.
