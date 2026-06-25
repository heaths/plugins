# AGENTS

## Architecture

Plugin marketplace for [GitHub Copilot CLI] and [Claude Code]. Defined in `.claude-plugin/marketplace.json`; each plugin lives under `plugins/<name>/`.

| File | Purpose |
| --- | --- |
| `.claude-plugin/marketplace.json` | Marketplace manifest with plugin versions and sources |
| `plugins/<name>/.claude-plugin/plugin.json` | Plugin details: name, description, version, author, skills |
| `plugins/<name>/skills/<skill-name>/SKILL.md` | Skill — YAML frontmatter (`name`, `description`, `compatibility`) + instructions |
| `plugins/<name>/.mcp.json` | MCP server configuration |

Skill paths in `plugin.json` are relative to the plugin directory (e.g., `"./skills/check-spelling"` resolves from `plugins/linting/`).

## Versioning

Plugin and marketplace versions are independent semver values in `marketplace.json`.

**Plugin version** — bump based on the most significant change:

| Change | Bump |
| --- | --- |
| Bug fix or docs update | patch |
| Add skill, MCP server, or tool | minor (reset patch) |
| Remove or rename skill, MCP server, or tool | major (reset minor + patch) |

**Marketplace version** — bump based on the most significant change:

| Change | Bump |
| --- | --- |
| Any plugin version bumped | patch |
| Plugin added | minor (reset patch) |
| Plugin removed | minor if 0.x.y; major once ≥ 1.0.0 (reset minor + patch) |

## Plugin metadata

**In-repository** (`source` is a local path): both `marketplace.json` and `plugin.json` require `name`, `description`, `version`, `author`; `plugin.json` also needs `category`, `keywords`.

**Remote** (`source.source == "github"`): `marketplace.json` requires `name`, `description`, `version`, `source` (`{source: "github", repo: "<owner>/<repo>"}`), `repository`, `author`, `license`, `category`, `keywords`. Do not duplicate skill or MCP server definitions locally.

## README maintenance

Keep the `README.md` **Plugins** section in sync with the marketplace:

1. **Add** a `### <plugin-name>` subsection (alphabetical) with description, skills table, and install commands for both CLIs.
2. **Remove** the subsection when a plugin is deleted from the marketplace.
3. **Update** description, skill names, and skill descriptions when they change in `plugin.json` or `SKILL.md` frontmatter.

## Pre-commit checklist

1. Plugin files changed → bump plugin `version` in both `marketplace.json` and `plugin.json`.
2. Plugin added or removed → bump marketplace `metadata.version` (minor for add; minor if 0.x.y or major otherwise for remove).
3. Only plugin version bumped → increment marketplace `metadata.version` patch.

## Commits and pull requests

Use a brief, human-readable title — no conventional prefixes (`feat:`, `fix:`, `chore:`, etc.). Add a body when the title alone isn't sufficient.

## Conventions

- Skill names in YAML frontmatter must match their directory name exactly.
- SKILL.md frontmatter fields should not end with a trailing period.
- Line endings are LF (enforced by `.gitattributes` and `.editorconfig`).
- JSON files use 2-space indentation.
- Scripts defined by skills must be written in Python.
- Each plugin maintains a single venv for all its skills at `plugins/<name>/.venv`. Skills must instruct the agent to create it with `python -m venv <plugin-dir>/.venv`, install dependencies from the skill's `requirements.txt`, and invoke scripts via `<plugin-dir>/.venv/bin/python`.

[GitHub Copilot CLI]: https://github.com/features/copilot/cli/
[Claude Code]: https://claude.ai/code
