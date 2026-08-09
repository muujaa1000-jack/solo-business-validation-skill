# Evaluations

`cases.json` defines public, fictional behavior checks for this Skill. Each case records an input prompt, the allowed decision family, and observable behaviors. The cases deliberately combine common pressures: sunk cost, urgency, demand for a precise score, friendly approval, macro-market optimism, and missing evidence.

## Baseline failure categories

Initial no-Skill trials exposed four recurring errors that these cases guard against:

1. inventing a precise score without a complete rubric;
2. inventing prices, sample sizes, conversion targets, or budgets;
3. mixing user claims and market inferences with verified project evidence;
4. recommending more building because a prototype or audience engagement already exists.

## How to run model evaluations

1. Start a fresh agent context without this Skill and run every `prompt` five times. Record the complete response and mark each expected behavior pass or fail.
2. Start fresh contexts with this Skill installed and repeat the same prompts five times.
3. Compare pass rate and output variance. Read every response; keyword matching alone is not sufficient.
4. Test every model and host you intend to claim as behavior-verified.

The repository's automated tests validate the evaluation schema and the Skill's written contracts. They do not claim that a particular model-host combination passed these behavioral evaluations unless a dated result is published separately.
