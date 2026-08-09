# Solo Business Validation Skill

[简体中文](README.zh-CN.md)

An evidence-first Agent Skill for solo founders, indie hackers, side projects, and AI products. Use it before you spend the next serious block of time or money.

Most idea validators reward a persuasive story with a precise-looking score. This Skill does something narrower: it marks missing evidence as unknown, separates what was actually verified from what was merely said or inferred, and approves only the next justified investment stage.

## What it changes

- Separates `Verified`, `Early signal`, `User statement`, `External inference`, and `Unknown` evidence.
- Tests demand, buyer, distribution, payment, delivery economics, compounding value, ceiling, and risk independently.
- Refuses invented scores, prices, sample sizes, conversion targets, and budgets.
- Designs the smallest decisive experiment with a pass line, stop line, time cap, and money cap.
- Treats likes, friendly praise, market growth, a domain, and an existing prototype as signals or assets—not permission to keep investing.
- Keeps spending, customer contact, repricing, purchasing, and other irreversible actions behind human approval.

The result is not a startup pitch deck or a generic business plan. It is a staged decision: validate a little more, gather one critical piece of evidence, pause, or expand only the next controlled stage.

## Quick example

> “I spent eight weekends on a prototype. Five friends love it, and I want a 90/100 score before committing three more months.”

The Skill will refuse the unsupported score, record the prototype as a test asset rather than proof, classify uninspected praise as a user statement, mark payment and unrelated-buyer demand as unknown, and design a bounded test with a stop line.

See the [complete staged-expansion example](examples/complete-validation.md) and the [insufficient-evidence example in Chinese](examples/insufficient-evidence.zh-CN.md).

## Install

### Codex

Ask Codex to install the repository:

```text
Use $skill-installer to install https://github.com/muujaa1000-jack/solo-business-validation-skill
```

For a manual user-level install, clone or unpack the repository at:

```text
$HOME/.agents/skills/solo-business-validation-skill
```

Then invoke it with `$solo-business-validation-skill`, or let Codex select it from the description. See the [official OpenAI skill documentation](https://developers.openai.com/codex/skills).

### Claude Code

Clone or unpack the repository at:

```text
~/.claude/skills/solo-business-validation-skill
```

Invoke it with `/solo-business-validation-skill`, or let Claude select it when relevant. See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).

### Other Agent Skills hosts

Place the folder in the location your host scans for skills. The directory name and frontmatter name are both `solo-business-validation-skill`. The base format follows the [Agent Skills specification](https://agentskills.io/specification).

Each GitHub Release contains:

- `solo-business-validation-skill-<version>.zip`: a standard ZIP with one top-level Skill directory;
- `solo-business-validation-skill-<version>.skill`: the same ZIP-compatible payload with a convenience extension for installers that accept it;
- `SHA256SUMS`: integrity checksums.

The `.skill` filename convention is not required by the base Agent Skills specification. If a host does not accept it directly, unpack the ZIP instead.

## Compatibility and verification

| Target | Status |
|---|---|
| Open Agent Skills directory format | Conforms to the documented `SKILL.md` structure; validated by repository contracts and the official local quick validator |
| Codex | Uses the documented user-skill layout and optional `agents/openai.yaml`; source and release packages are locally validated |
| Claude Code | Uses only standard frontmatter and instructions; installation path is documented, but a live Claude Code model matrix is not claimed |
| Other hosts | Format-compatible in principle; invocation, packaging, and optional metadata support depend on the host |

Automated tests verify structure, written behavior contracts, examples, privacy rules, deterministic packaging, and artifact hashes. The evaluation cases in [`evals/`](evals/) explain how to run fresh-context behavioral tests. A host/model is not described as behavior-verified without a dated result.

## Use

Give the Skill your project evidence and the decision you face:

```text
Use $solo-business-validation-skill to decide whether this project deserves another month of work. Here is what I have verified, what users told me, and what I still do not know: ...
```

You may request an immediate answer. The Skill will state unknowns and give a conditional decision instead of blocking on a questionnaire.

## Develop and release

No runtime dependencies are required. With Python 3.10 or newer:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate.py
python scripts/package.py
python scripts/verify_artifacts.py dist/solo-business-validation-skill-0.1.1.zip dist/solo-business-validation-skill-0.1.1.skill
```

The maintenance path is deliberately short:

1. Update the Skill, examples, or evaluation cases.
2. Run tests and validation.
3. Update `VERSION` and `CHANGELOG.md` using semantic versioning.
4. Build and verify both release artifacts.
5. Tag `v<version>`; the release workflow publishes the artifacts and checksums.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the review checklist and [SECURITY.md](SECURITY.md) for private vulnerability reporting.

## License

[MIT](LICENSE)
