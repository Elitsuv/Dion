---
name: cli-tool-scaffolder
description: Scaffolds ergonomic command-line utility tools in Python, Go, or Rust with argument parsing and subcommands. Use when building developer tools.
---

# CLI Tool Scaffolder

## Protocol
1. Spec -> Define subcommands, args, and flags.
2. Scaffold -> Write script with argparse or click.
3. Ergonomics -> Add help, exit codes, and stderr.

## Guardrails
- Never output filler or pleasantries.
- Never send diagnostic errors to stdout; use stderr.
- Never omit --help argument specifications.

## Output Schema
### CLI Implementation
- Command: `tool <cmd> [flags] <args>`
[Self-contained executable script]
- Test: `tool --help`
