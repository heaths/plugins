# Contributing

This repository keeps plugin evals under `evals/` and uses [Vally](https://microsoft.github.io/vally/) to lint specs, run the pull request eval suite, and compare experiment variants.

Run commands from the repository root.

## Prerequisites

Install the pinned CLI dependencies:

```sh
npm i
```

Authenticate Copilot once before running evals or experiments:

```sh
copilot
# then run /login
```

## Common development tasks

### Lint eval specs

Use this before sending a change for review:

```sh
vally lint --eval-spec evals
```

### Run the pull request eval suite

The `pr` suite is defined in `.vally.yaml` and currently runs eval stimuli tagged with `priority: p0`.

```sh
vally eval --suite pr --output-dir vally-results --junit
```

### Run a single eval file

When iterating on one plugin's coverage, point Vally at that spec directly:

```sh
vally eval --eval-spec evals/security/eval.yaml --output-dir vally-results
```

## Experiments

Use experiments when you want to compare variants of the same eval. The current
`pin-github-actions` benchmark compares the scripted skill in this repository
with the pre-script, instruction-only baseline maintained on the
`experiments-baseline` branch.

### Experiment layout

- Put experiments under a dedicated directory such as
  `evals/security/pin-github-actions-usage/`.
- Keep related helper scripts in that same experiment directory.
- Add a concise root `package.json` script for each helper, and keep repo helper
  scripts in ES module format.

### Prepare the baseline worktree

Create the local worktree once:

```sh
git worktree add .worktrees/experiments-baseline experiments-baseline
```

Refresh it later as needed:

```sh
git -C .worktrees/experiments-baseline pull --ff-only
```

### Preview the experiment plan

```sh
vally experiment run evals/security/pin-github-actions-usage/experiment.yaml --dry-run
```

### Run the pin-github-actions usage experiment

```sh
vally experiment run \
  evals/security/pin-github-actions-usage/experiment.yaml \
  --output-dir vally-experiment-results
```

### Summarize relative cost

Analyze the latest experiment run:

```sh
npm run pin-github-actions-experiment:compare
```

Analyze a specific run directory:

```sh
npm run pin-github-actions-experiment:compare -- vally-experiment-results/2026-06-26T05-33-51-234Z
```

The experiment writes one directory per variant under the timestamped run folder.
Compare `results.jsonl` and `run-summary.jsonl` for `scripted-main` and
`skill-only-baseline` to see whether the scripted skill reduces model calls,
tokens, or cost. The baseline variant loads its skill from
`.worktrees/experiments-baseline/`, so keep that branch available locally before
running the comparison.

## More information

See the [Vally documentation](https://microsoft.github.io/vally/) for the full eval, suite, and experiment reference.
