# Agent plugins

## Installation

To install this marketplace into [GitHub Copilot CLI] run:

```bash
copilot plugin marketplace add heaths/plugins
```

## Plugins

### azsdk-samples-mcp

Discovers and retrieves code samples from Azure SDK packages in .NET, Node.js, and Rust projects.

```bash
copilot plugin install azsdk-samples-mcp@heaths-plugins
```

### linting

Skills and tools for formatting and linting.

| Skill | Description |
| --- | --- |
| check-spelling | Check and fix spelling in project source files using cSpell |
| lint-markdown | Check and fix formatting and other issues in markdown files using markdownlint-cli2 |

```bash
copilot plugin install linting@heaths-plugins
```

## License

Licensed under the [MIT](LICENSE.txt) license.

[GitHub Copilot CLI]: https://github.com/features/copilot/cli/
