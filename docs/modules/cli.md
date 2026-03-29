---
type: documentation
entity: module
module: "cli"
version: 1.0
---

# Module: cli

> Part of [Agent Skills Hub](../overview.md)

## Overview

### Responsibility

The CLI module provides the `npx @flitzrrr/agent-skills` command for installing, updating, and listing skills. It clones the repo to `~/.agent-skills/` and creates symlinks into each platform's skill directory.

IS responsible for: cloning the repo, creating platform-specific symlinks, listing available skills.
IS NOT responsible for: building the catalog, syncing documentation, or discovering new skills.

### Dependencies

| Dependency | Type     | Purpose                                             |
| ---------- | -------- | --------------------------------------------------- |
| git        | external | Cloning and updating the repository                 |
| Node.js    | external | Runtime (stdlib only — fs, path, os, child_process) |

## Structure

| Path             | Type | Purpose                                                           |
| ---------------- | ---- | ----------------------------------------------------------------- |
| `bin/cli.js`     | file | Main CLI entry point, registered as `agent-skills` bin in npm     |
| `bin/test-cli.js`| file | Test suite for CLI (syntax validation + functional tests)         |
| `package.json`   | file | npm package manifest — defines bin entry, version, published files|

## Key Symbols

| Symbol             | Kind     | Visibility | Location             | Purpose                                                    |
| ------------------ | -------- | ---------- | -------------------- | ---------------------------------------------------------- |
| `PLATFORMS`        | const    | internal   | `bin/cli.js:11`      | Platform config map — name, skill directory, notes          |
| `REPO_URL`         | const    | internal   | `bin/cli.js:8`       | GitHub clone URL for the agent-skills repository            |
| `SKILL_DIR`        | const    | internal   | `bin/cli.js:9`       | Local installation path (`~/.agent-skills`)                 |
| `cloneRepo`        | function | internal   | `bin/cli.js:44`      | Clones repo or pulls updates if already present             |
| `installForPlatform` | function | internal | `bin/cli.js:61`      | Creates symlinks from skills/ into a platform's skill dir   |
| `listSkills`       | function | internal   | `bin/cli.js:102`     | Reads skills dir and prints sorted list                     |

## Data Flow

1. User runs `npx @flitzrrr/agent-skills install [platform]`
2. `cloneRepo()` clones or pulls the repo to `~/.agent-skills/`
3. For each platform (or specified platform), `installForPlatform()` creates symlinks from `~/.agent-skills/skills/*` into the platform's skill directory
4. Existing symlinks are preserved (skip, no overwrite)

## Configuration

- **`SKILL_DIR`**: Hardcoded to `~/.agent-skills` — not configurable
- **`PLATFORMS`**: Defines 5 platforms (claude, antigravity, codex, opencode, cursor) with their skill directories

## Inventory Notes

- **Coverage**: full
- **Notes**: Single-file module. All logic in `bin/cli.js`.
