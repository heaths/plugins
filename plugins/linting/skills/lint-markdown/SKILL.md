---
name: lint-markdown
description: Check and fix formatting and other issues in markdown files using markdownlint-cli2
---

# Markdown linting

Check markdown files for common mistakes.

## Installation and usage

Search for a `package.json` in the current working directory and each ancestor directory up to and including the repository root.

If an ancestor `package.json` has `markdownlint-cli2` in `devDependencies`, run `npm install` from that `package.json` directory to install it, then run `npx markdownlint-cli2 <command>` from the current working directory.

If no ancestor `package.json` contains `markdownlint-cli2` in `devDependencies`, run `npx -y markdownlint-cli2 <command>` from the current working directory instead. Do not add `markdownlint-cli2` to any `package.json` or install it permanently.

## Configuration

markdownlint-cli2 configuration including custom rules can be found in files:

- `.markdownlint-cli2.json`
- `.markdownlint-cli2.yaml`
- `.markdownlint-cli2.yml`

If a suitable configuration is not found, create a `.markdownlint-cli2.yaml` file in the root of the repository.
The configuration file schema is described at `https://raw.githubusercontent.com/DavidAnson/markdownlint-cli2/v<version>/schema/markdownlint-cli2-config-schema.json` where `<version>` should match the `markdownlint-cli2` version from the ancestor `package.json` `devDependencies` (e.g., `v0.20.0`). If no ancestor `package.json` contains `markdownlint-cli2` in `devDependencies`, use `https://raw.githubusercontent.com/DavidAnson/markdownlint-cli2/main/schema/markdownlint-cli2-config-schema.json`.
Always include the schema URI in the `$schema` field.

For markdownlint rules configuration, nest it under the `config` property following the markdownlint schema at `https://raw.githubusercontent.com/DavidAnson/markdownlint/main/schema/markdownlint-config-schema.json`.

If not already present, add a `globs` array with file patterns to lint (e.g., `["**/*.md"]`) so no command-line arguments are needed.

## Check Markdown

By default, check only markdown files changed since the last commit:

```bash
npx markdownlint-cli2 --no-globs $(git diff --name-only --diff-filter=d HEAD -- '*.md' '*.markdown')
```

`--no-globs` prevents falling back to config globs when no files match.

To check all files (when explicitly asked):

```bash
npx markdownlint-cli2
```

## Fix issues

By default, fix only markdown files changed since the last commit:

```bash
npx markdownlint-cli2 --no-globs --fix $(git diff --name-only --diff-filter=d HEAD -- '*.md' '*.markdown')
```

To fix all files (when explicitly asked):

```bash
npx markdownlint-cli2 --fix
```

Unfixable issues: show the output to the user and ask what to do.

## Testing

Run the same check command again to verify all issues are fixed. There should be no errors reported.
