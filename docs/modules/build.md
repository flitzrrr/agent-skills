---
type: documentation
entity: module
module: "build"
version: 1.0
---

# Module: build

> Part of [Agent Skills Hub](../overview.md)

## Overview

### Responsibility

The build module provides scripts that keep repository metadata, platform config files, the GitHub Pages catalog, and the GitHub Wiki in sync with the current state of `skills/` and `vendor/`.

IS responsible for: counting skills/sources, updating badge counts, regenerating catalog.json, syncing platform config files, pushing wiki updates.
IS NOT responsible for: installing skills (CLI module), discovering new sources (CI/CD module), or linting.

### Dependencies

| Dependency  | Type     | Purpose                                       |
| ----------- | -------- | --------------------------------------------- |
| Node.js     | external | Runtime (stdlib only — fs, path, child_process)|
| git         | external | Wiki clone/push, reading repo state           |
| `docs/catalog.json` | internal | Input for wiki generation, output of build-catalog |

## Structure

| Path                   | Type | Purpose                                                             |
| ---------------------- | ---- | ------------------------------------------------------------------- |
| `bin/build-catalog.js` | file | Builds `docs/catalog.json` from SKILL.md frontmatter across all skills |
| `bin/sync-docs.js`     | file | Syncs skill/source counts across README, AGENTS.md, CLAUDE.md, .cursorrules, .lovable, CHEATSHEET.md |
| `bin/update-wiki.js`   | file | Regenerates GitHub Wiki Skills-Catalog page from catalog.json       |
| `bin/sync-skills.sh`   | file | Shell script for skill symlink synchronization (untracked)          |
| `docs/catalog.json`    | file | Generated catalog — skill names, sources, descriptions              |
| `docs/index.html`      | file | GitHub Pages searchable catalog UI                                  |

## Key Symbols

### build-catalog.js

| Symbol              | Kind     | Visibility | Location                  | Purpose                                                     |
| ------------------- | -------- | ---------- | ------------------------- | ----------------------------------------------------------- |
| `findSkillMd`       | function | internal   | `bin/build-catalog.js:19` | Recursively searches for SKILL.md in a directory (max depth) |
| `extractDescription`| function | internal   | `bin/build-catalog.js:40` | Parses YAML frontmatter or first paragraph for description   |
| `descFromName`      | function | internal   | `bin/build-catalog.js:103`| Generates fallback description from skill name               |
| `main`              | function | internal   | `bin/build-catalog.js:141`| Iterates all skills, builds catalog array, writes JSON       |

### sync-docs.js

| Symbol | Kind     | Visibility | Location              | Purpose                                                       |
| ------ | -------- | ---------- | --------------------- | ------------------------------------------------------------- |
| (main) | script   | internal   | `bin/sync-docs.js:19` | Counts skills/sources, regex-replaces counts in 6 config files |

### update-wiki.js

| Symbol   | Kind     | Visibility | Location                | Purpose                                              |
| -------- | -------- | ---------- | ----------------------- | ---------------------------------------------------- |
| `groupBy`| function | internal   | `bin/update-wiki.js:24` | Groups catalog entries by source for wiki generation  |
| `main`   | function | internal   | `bin/update-wiki.js:33` | Clones wiki repo, generates markdown, commits & pushes|

## Data Flow

```
skills/ directory
    │
    ▼
build-catalog.js ──► docs/catalog.json
    │                       │
    ▼                       ▼
sync-docs.js           update-wiki.js
    │                       │
    ▼                       ▼
README.md              GitHub Wiki
AGENTS.md              (Skills-Catalog.md)
CLAUDE.md
.cursorrules
.lovable
CHEATSHEET.md
```

## Configuration

- No environment variables required for local use
- `update-wiki.js` requires SSH access to the wiki repo (`git@github.com:flitzrrr/agent-skills.wiki.git`)

## Inventory Notes

- **Coverage**: full
- **Notes**: All scripts are stdlib-only Node.js. `sync-skills.sh` is untracked and appears to be a local utility.
