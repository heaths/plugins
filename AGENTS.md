# AGENTS

## Architecture

This is a GitHub Copilot CLI plugin marketplace. The marketplace is defined in `.github/plugin/marketplace.json` and contains multiple plugins, each under `plugins/<name>/`. Plugins can declare skills (prompt-based capabilities in `SKILL.md` files) and MCP servers (in `.mcp.json` files).

### Key files

- `.github/plugin/marketplace.json` — marketplace manifest listing all plugins with their versions and sources.
- `plugins/<name>/.github/plugin/plugin.json` — per-plugin details including name, description, version, author, and skills.
- `plugins/<name>/skills/<skill-name>/SKILL.md` — skill definition with YAML frontmatter (`name`, `description`, `compatibility`) and markdown instructions.
- `plugins/<name>/.mcp.json` — MCP server configuration for a plugin.

### Skill paths

Skill paths in `plugin.json` are relative to the plugin directory (e.g., `"./skills/check-spelling"` resolves from `plugins/linting/`).

## Versioning

The marketplace and each plugin have independent semver versions in `marketplace.json`. When making changes:

### Plugin versions

- Bump the **patch** version for bug fixes or documentation changes to existing skills, MCP servers, or other plugin files.
- Bump the **minor** version (and reset patch to 0) when adding new skills, MCP servers, or tools to a plugin.
- Bump the **major** version (and reset minor and patch to 0) when removing or renaming skills, MCP servers, or tools.

### Marketplace version

- Bump the **patch** version when any plugin version is bumped.
- Bump the **minor** version (and reset patch to 0) when a plugin is added to the marketplace.
- Bump the **major** version (and reset minor and patch to 0) when a plugin is removed from the marketplace.

> **Note:** For 0.x.y releases (before 1.0.0), a minor version bump is semantically equivalent to a major version bump. Use a minor bump for removals instead of bumping to 1.0.0.

## Plugin metadata

### In-repository plugins

Plugins that live in this repository (`source` is a local path like `"plugins/<name>"`) should include the following fields in both `marketplace.json` and their `plugins/<name>/.github/plugin/plugin.json`:

- `name`, `description`, `version`, `author` — required everywhere
- `category`, `keywords` — include in `plugin.json` for discoverability

### Remote plugins

Plugins sourced from an external GitHub repository (`source` is an object with `"source": "github"`) should include the following fields in `marketplace.json`:

- `name`, `description`, `version` — basic identity
- `source` — object with `"source": "github"` and `"repo": "<owner>/<repo>"`
- `repository` — full URL to the repository (e.g., `"https://github.com/<owner>/<repo>"`)
- `author`, `license`, `category`, `keywords` — copy from the remote plugin's `.github/plugin/plugin.json` for discoverability

The remote repository owns its own `plugin.json`; do not duplicate skill or MCP server definitions locally.

## Pre-commit checklist

Before committing, verify:

1. If any files under `plugins/<name>/` changed, that plugin's `version` in both `marketplace.json` and `plugins/<name>/.github/plugin/plugin.json` has been bumped following semver rules above.
2. If a plugin was added or removed from the marketplace, the marketplace `metadata.version` has been bumped accordingly (minor for additions, minor for removals if still 0.x.y, or major for removals once 1.0.0 or later).
3. Otherwise, if any plugin version was bumped, the marketplace `metadata.version` patch version has been incremented.

## Commits and pull requests

Commit messages and pull request titles should be a brief, human-readable summary of the change. Do not use conventional commit prefixes like `feat:`, `fix:`, `chore():`, etc.

The commit or pull request body should provide additional context when the title alone is not sufficient to explain the change.

## Conventions

- Skill names in YAML frontmatter must match their directory name exactly.
- SKILL.md frontmatter fields should not end with a trailing period.
- Line endings are LF (enforced by `.gitattributes` and `.editorconfig`).
- JSON files use 2-space indentation.
