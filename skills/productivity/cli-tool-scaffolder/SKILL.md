---
name: cli-tool-scaffolder
description: Scaffolds ergonomic command-line utility tools in Python, Go, or Rust with argument parsing, subcommands, and help text. Use when building developer tools.
---

# CLI Tool Scaffolder

Scaffold production-grade, ergonomic command-line utilities with argument parsers, subcommands, and structured output.

## Trigger Conditions

Activate this skill when:
- A user wants to build a CLI utility script or developer tool.
- A student asks: 'Scaffold a Python CLI with argparse/click', 'Build a command-line tool in Go/Rust', or 'Create a CLI script with flags and subcommands'.

## Execution Protocol

Follow standard CLI design ergonomics:

### 1. Command-Line Interface Specification
- Define command name, arguments, options, and flags:
  - Positional arguments (required inputs).
  - Optional flags with short and long formats (`-v`, `--verbose`).
  - Subcommands for distinct operations (e.g., `tool run`, `tool status`, `tool config`).

### 2. Standard Library Implementation
- Provide a clean, robust implementation using standard or canonical libraries (e.g., `argparse` in Python, `flag` in Go, `clap` in Rust):
  - Meaningful help descriptions for all flags.
  - Input validation and informative error messages on invalid flags.
  - Proper exit codes (`0` for success, non-zero for errors).

### 3. Structured Output & Verbosity
- Support clean formatted output:
  - Quiet mode (`-q`, `--quiet`) for scripting and pipes.
  - Verbose mode (`-v`, `--verbose`) for debugging.

## Output Quality Rules

- Keep implementation self-contained and immediately runnable.
- Follow Unix CLI conventions (help flag `-h/--help`, standard error stream for diagnostics).
