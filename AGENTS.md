# AGENTS

## Architecture

This is a GitHub Copilot CLI plugin marketplace. The marketplace is defined in `.github/plugin/marketplace.json` and contains multiple plugins, each under `plugins/<name>/`. Plugins can declare skills (prompt-based capabilities in `SKILL.md` files) and MCP servers (in `.mcp.json` files).

### Key files

- `.github/plugin/marketplace.json` — marketplace manifest listing all plugins with their versions, sources, and skill/tool paths.
- `plugins/<name>/skills/<skill-name>/SKILL.md` — skill definition with YAML frontmatter (`name`, `description`, `compatibility`) and markdown instructions.
- `plugins/<name>/.mcp.json` — MCP server configuration for a plugin.

### Skill paths

Skill paths in `marketplace.json` are relative to the plugin `source` directory (e.g., `"./skills/check-spelling"` resolves from `plugins/linting/`).

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

## Pre-commit checklist

Before committing, verify:

1. If any files under `plugins/<name>/` changed, that plugin's `version` in `marketplace.json` has been bumped following semver rules above.
2. If a plugin was added or removed from the marketplace, the marketplace `metadata.version` has been bumped accordingly (minor for additions, major for removals).
3. Otherwise, if any plugin version was bumped, the marketplace `metadata.version` patch version has been incremented.

## Conventions

- Skill names in YAML frontmatter must match their directory name exactly.
- SKILL.md frontmatter fields should not end with a trailing period.
- Line endings are LF (enforced by `.gitattributes` and `.editorconfig`).
- JSON files use 2-space indentation.
