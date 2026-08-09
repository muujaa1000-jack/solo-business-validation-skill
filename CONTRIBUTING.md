# Contributing

Contributions that make the Skill clearer, safer, more evidence-bound, or easier to validate are welcome.

## Before opening a pull request

1. Keep the Skill focused on solo-business investment decisions. Do not turn it into a general startup-consulting toolkit.
2. Add or update an evaluation case before changing behavior.
3. Keep examples fictional or clearly composite. Never include private customer, store, transaction, product, or account data.
4. Do not add a runtime dependency unless the behavior cannot be expressed safely as instructions.
5. Run:

   ```bash
   python -m unittest discover -s tests -p "test_*.py" -v
   python scripts/validate.py
   python scripts/package.py
   python scripts/verify_artifacts.py dist/solo-business-validation-skill-0.1.0.zip dist/solo-business-validation-skill-0.1.0.skill
   ```

6. Check that `SKILL.md` remains under 500 lines and uses only forward-slash relative paths.
7. Update `CHANGELOG.md` when the change is user-visible.

## Pull-request checklist

- [ ] The change has a corresponding contract or evaluation.
- [ ] Missing evidence remains unknown rather than becoming a score.
- [ ] Prices, sample sizes, budgets, and thresholds are derived or clearly marked provisional.
- [ ] Pass line, stop line, time cap, and money cap remain explicit.
- [ ] Spending and irreversible actions remain human-gated.
- [ ] No credential, private data, identifying business detail, or machine-specific path is included.
- [ ] Source and both release artifacts pass validation.

Use small commits with clear messages. Maintainers may ask for a narrower change if a pull request mixes unrelated documentation, behavior, and tooling updates.
