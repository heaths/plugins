---
name: pin-github-actions
description: Run when adding or updating GitHub Actions workflow steps. Pin every action to a commit SHA with the resolved version tag as a trailing comment.
---

# Pin GitHub Actions

Use the script as the source of truth. Run it first; only fall back to manual reasoning
if the script fails or reports unresolved references.

The **skill directory** is the directory containing this SKILL.md file. The
**plugin directory** is two levels above the skill directory (the parent of `skills/`).

## Default flow

Run from the root of the repository whose workflows you want to pin.

Create the plugin venv once if it does not already exist:

```bash
python -m venv <plugin-dir>/.venv
<plugin-dir>/.venv/bin/pip install -r <skill-dir>/scripts/requirements.txt
```

If `python` is unavailable, retry the same setup command with `python3`.

Prefer passing the specific workflow files you already know about:

```bash
<plugin-dir>/.venv/bin/python <skill-dir>/scripts/pin_github_actions.py .github/workflows/ci.yml
```

Pin every workflow under `.github/workflows/` only when you need a broader sweep:

```bash
<plugin-dir>/.venv/bin/python <skill-dir>/scripts/pin_github_actions.py
```

Do not read `pin_github_actions.py` or `requirements.txt` unless the command fails.
Do not hand-edit `uses:` lines unless the script cannot complete the change.
Treat a zero exit status as success.

## Rules

- Every non-local `uses:` step must end as `owner/action@<40-char-sha> # vX.Y.Z`.
- Never leave a mutable ref such as `@v4` or `@main`.
- Internal workflow references (`uses: ./.github/workflows/...`) are exempt and are not modified by the script.
