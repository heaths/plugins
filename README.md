# Agent plugins

## Installation

Plugins are compatible with both [GitHub Copilot CLI] and [Claude Code].

### GitHub Copilot CLI

To install this marketplace into [GitHub Copilot CLI] run:

```bash
copilot plugin marketplace add heaths/plugins
```

### Claude Code

To install this marketplace into [Claude Code] run:

```text
/plugin marketplace add heaths/plugins
```

## Sharing with contributors

You can recommend this marketplace and its plugins to everyone who works in a repository by committing a `.claude/settings.json` file to that repository. Contributors whose [Claude Code] session picks up the file will automatically have the marketplace registered and can install plugins from it.

Example `.claude/settings.json`:

```json
{
  "plugins": [
    "linting@heaths-plugins"
  ]
}
```

> **Note:** [GitHub Copilot CLI] does not currently support project-level plugin recommendations. Contributors using Copilot CLI should run the marketplace and plugin install commands above individually.

## Plugins

### azsdk-samples-mcp

Discovers and retrieves code samples from Azure SDK packages in .NET, Node.js, and Rust projects.

```bash
# GitHub Copilot CLI
copilot plugin install azsdk-samples-mcp@heaths-plugins
```

```text
# Claude Code
/plugin install azsdk-samples-mcp@heaths-plugins
```

### linting

Skills and tools for formatting and linting.

| Skill | Description |
| --- | --- |
| check-spelling | Check and fix spelling in project source files using cSpell |
| lint-markdown | Check and fix formatting and other issues in markdown files using markdownlint-cli2 |

```bash
# GitHub Copilot CLI
copilot plugin install linting@heaths-plugins
```

```text
# Claude Code
/plugin install linting@heaths-plugins
```

## License

Licensed under the [MIT](LICENSE.txt) license.

[GitHub Copilot CLI]: https://github.com/features/copilot/cli/
[Claude Code]: https://claude.ai/code
