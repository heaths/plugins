---
name: check-spelling
description: Check and fix spelling in project source files using cSpell
---

# Spell checking

## Installation and usage

Search for a `package.json` in the current working directory and each ancestor directory up to and including the repository root.

If an ancestor `package.json` has `cspell` in `devDependencies`, run `npm install` from that `package.json` directory to install it, then run `npx cspell <command>` from the current working directory.

If no ancestor `package.json` contains `cspell` in `devDependencies`, run `npx -y cspell <command>` from the current working directory instead. Do not add `cspell` to any `package.json` or install it permanently.

## Configuration

cSpell configuration including custom dictionaries and word lists can be found in files:

- `cspell.json`
- `cspell.config.json`
- `cspell.yaml` or `cspell.yml`
- `cspell.config.yaml` or `cspell.config.yml`

They may be prefaced with an optional `.` or in a `.config/` directory e.g.:

- `.cspell.json`
- `.config/cspell.yaml`
- `.config/.cspell.yml`

They may also be located in a `.vscode/` directory e.g.:

- `.vscode/cspell.json`

If a suitable configuration is not found, create a `.cspell.json` file in the root of the repository.
The configuration file schema is described at `https://raw.githubusercontent.com/streetsidesoftware/cspell/v<version>/cspell.schema.json` where `<version>` should match the `cspell` version from the ancestor `package.json` `devDependencies` (e.g., `v9.6.2`). If no ancestor `package.json` contains `cspell` in `devDependencies`, use `https://raw.githubusercontent.com/streetsidesoftware/cspell/main/cspell.schema.json`.
Always include the schema URI in the `$schema` field and set the current project language e.g., "en".
Inside a git repository you should also set `useGitignore` to `true` in the configuration file.

When running any cspell command, pass `--config <path>` with the path to the configuration file.

## Check spelling

Run `npx cspell lint [options] [globs...]` to check a list of file globs or `.` for the directory tree.

## Fix spelling

Show a summary of the misspelling to the user. Prompt the user for which words should be replaced with another word. All remaining words should be added to the dictionary using the steps below.

### Choosing the correct configuration file for dictionary words

A project may have multiple cspell configuration files at different directory levels. When adding a word to the `words` array, select the configuration file as follows:

1. For each file that contains the misspelling, find the nearest cspell configuration file by searching from that file's directory upward through ancestor directories to the repository root.
2. If all files resolve to the same configuration file, add the word there.
3. If files resolve to different configuration files, find the nearest common ancestor directory of those files. Search from that ancestor directory upward for an existing cspell configuration file and add the word there.
4. If no ancestor configuration file exists above the common ancestor directory, add the word to the root configuration file.

This prevents the same word from being duplicated across multiple configuration files.

### Overrides

If any misspellings are only in files that match any `filename` globs in an optional `overrides` section of the chosen configuration file, add those words to the `words` array in that override according to the schema.

### Inline ignores

Seldom used words can be ignored within the file they are used by adding an appropriate comment e.g.:

```js
// cspell:ignore <word>
```

## Testing

Run the same command again used to check spelling. All misspellings should be fixed.
