---
name: evaluate-skills
description: Use when creating, updating, or reviewing Vally evals for plugin skills. Covers eval.yaml, fixtures, graders, expect_skills, suites, tags, and eval coverage for new or changed skills.
---

# Evaluate plugin skills

Use the [Vally reference docs](https://microsoft.github.io/vally/) for schema and grader details.

This repo keeps evals under `evals/` and currently uses `.vally.yaml` to define the `pr`
suite from evals tagged with `priority: p0`.

Before running Vally commands in this repo, run `npm i` from the repository root so
`npx vally` and `npx copilot` use the pinned local versions from `package.json`.

## Layout

```text
.vally.yaml
evals/
├── <plugin-name>/
│   ├── eval.yaml
│   └── fixtures/
│       └── <scenario>/
│           └── ...
└── ...
```

- Each plugin keeps its eval spec in `evals/<plugin-name>/eval.yaml`.
- Put sample inputs under `evals/<plugin-name>/fixtures/`.
- Seed fixture files into the eval environment with `environment.files`.
- Keep experiment helper scripts in the experiment directory and expose them through
  an appropriately named root `package.json` script.
- Write repo experiment helper scripts as ES modules.

## When to use this skill

Use this skill when the request involves:

- adding evals for a new plugin skill
- updating evals after changing an existing plugin skill
- writing or editing `evals/<plugin-name>/eval.yaml`
- defining fixtures, graders, `expect_skills`, tags, or suites
- checking whether plugin-skill coverage is missing

## Writing evals

1. Add or update `evals/<plugin-name>/eval.yaml` with `name`, `version`,
   `description`, `tags`, `defaults`, `scoring`, and `stimuli`.
2. Define one or more `stimuli` with a realistic user `prompt`, the skill path in
   `environment.skills`, and any seeded files in `environment.files`.
3. Use skill paths relative to the eval file, for example
   `../../plugins/linting/skills/check-spelling`.
4. Add `constraints.expect_skills` so the eval asserts the intended skill was used.
5. Prefer outcome-based `graders` such as `file-matches`, `file-not-matches`, and
   `file-exists`.
6. Keep fixtures small and assertions specific to the behavior the skill should change.

## Configuring evals

1. Keep `.vally.yaml` in sync if you add new suites or change how evals are grouped.
2. Use eval `tags` for suite filters such as the current `priority: p0` pull request
   suite.
3. Run `npm i` from the repository root before invoking repo CLI tools.
4. Lint specs with `npx vally lint --eval-spec evals`.
5. Run the pull request suite with `npx vally eval --suite pr --output-dir vally-results --junit`.

## Coverage rule

When adding a new plugin skill, or materially changing an existing plugin skill's
behavior, add or update eval coverage in the corresponding `evals/<plugin-name>/`
directory as part of the same change.
