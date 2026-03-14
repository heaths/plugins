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

You can recommend this marketplace and its plugins to everyone who works in a repository by committing a `.claude/settings.json` file to that repository. When contributors trust the project folder in [Claude Code], they are prompted to install the marketplace and any enabled plugins.

Example `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "heaths-plugins": {
      "source": {
        "source": "github",
        "repo": "heaths/plugins"
      }
    }
  },
  "enabledPlugins": {
    "linting@heaths-plugins": true
  }
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
