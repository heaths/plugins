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

## GitHub Actions authentication

The eval workflow uses the short-lived `GITHUB_TOKEN` created for each workflow
run. It grants only `contents: read` and `copilot-requests: write`; no personal
access token (PAT) or repository secret is normally required.

The workflow pins a recent `@github/copilot` version because older versions
treated the Actions token as a user PAT and failed with an error such as:

```text
Failed to fetch PAT user login (401): GitHub returned: Bad credentials
```

If this authentication error recurs:

1. Confirm that the workflow grants `copilot-requests: write` and passes
   `${{ github.token }}` as `GITHUB_TOKEN`.
2. Confirm with an organization owner that **Allow use of Copilot CLI billed to
   the organization** is enabled.
3. Install the dependencies from the lockfile and confirm the pinned CLI is
   current:

   ```sh
   npm ci
   npx copilot --version
   ```

4. Re-run the failed workflow:

   ```sh
   gh run rerun <run-id> --failed --repo heaths/plugins
   ```

### PAT fallback

Use a PAT only when the organization policy cannot be enabled. Create a
fine-grained PAT owned by your personal account with the **Copilot Requests**
account permission set to **Read**. Classic PATs (`ghp_`) are not supported.
These evals do not need repository permissions on that PAT because checkout
uses the workflow's `GITHUB_TOKEN`.

PAT creation, permission selection, and organization approval cannot be done
with `gh`; use the
[fine-grained PAT form](https://github.com/settings/personal-access-tokens/new?name=Copilot+requests+token&user_copilot_requests=read).
After creating the token, `gh` can store it as the Actions secret expected by
the fallback workflow:

```sh
gh secret set COPILOT_GITHUB_TOKEN --repo heaths/plugins
```

Do not add this secret unless the workflow is also changed to pass it as
`COPILOT_GITHUB_TOKEN`, which takes precedence over `GITHUB_TOKEN`.

## More information

See the [Vally documentation](https://microsoft.github.io/vally/) for the full eval, suite, and experiment reference.
