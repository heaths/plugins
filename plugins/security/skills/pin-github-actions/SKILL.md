---
name: pin-github-actions
description: Run when adding or updating GitHub Actions workflow steps. Pin every action to a commit SHA with the resolved version tag as a trailing comment.
---

# Pin GitHub Actions

Pin every `uses:` step in a workflow to an exact commit SHA with the resolved version tag
as a trailing comment so the intent is clear.

**Format:**

```yaml
uses: owner/action@<commit-sha> # vX.Y.Z
```

**Example:**

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

## Setup

This skill uses a Python script. The **skill directory** is the directory containing
this SKILL.md file. The **plugin directory** is two levels above the skill directory
(the parent of `skills/`).

Create the plugin venv once if it does not already exist:

```bash
python -m venv <plugin-dir>/.venv
<plugin-dir>/.venv/bin/pip install -r <skill-dir>/scripts/requirements.txt
```

## Running

Run from the root of the repository whose workflows you want to pin.

Pin all workflows under `.github/workflows/`:

```bash
<plugin-dir>/.venv/bin/python <skill-dir>/scripts/pin_github_actions.py
```

Pin specific workflow files:

```bash
<plugin-dir>/.venv/bin/python <skill-dir>/scripts/pin_github_actions.py .github/workflows/ci.yml
```

## Rules

- Never reference a mutable tag (e.g., `@v4`, `@main`).
- Never omit the version comment — it is the only human-readable clue to the pinned version.
- Dependabot keeps SHAs current; do not manually update SHAs unless Dependabot cannot reach the action.
- Internal workflow references (`uses: ./.github/workflows/...`) are exempt and are not modified by the script.
