---
type: documentation
entity: module
module: "ci-cd"
version: 1.0
---

# Module: ci-cd

> Part of [Agent Skills Hub](../overview.md)

## Overview

### Responsibility

The CI/CD module defines GitHub Actions workflows that automate skill discovery, submodule updates, code quality checks, and npm publishing.

IS responsible for: weekly auto-discovery of new skill repos, weekly submodule updates, linting via MegaLinter, npm publishing on version tags, wiki updates, issue reports.
IS NOT responsible for: the build scripts themselves (build module), the CLI (cli module), or skill content.

### Dependencies

| Dependency           | Type     | Purpose                                            |
| -------------------- | -------- | -------------------------------------------------- |
| `bin/sync-docs.js`   | internal | Called by workflows to sync counts after changes    |
| `bin/build-catalog.js` | internal | Called to rebuild catalog.json                    |
| GitHub API           | external | Search for trending repos, create issues/PRs        |
| npm registry         | external | Package publishing                                  |
| MegaLinter           | external | Markdown, YAML, JSON linting                        |

## Structure

| Path                                       | Type | Purpose                                                           |
| ------------------------------------------ | ---- | ----------------------------------------------------------------- |
| `.github/workflows/skill-discovery.yml`    | file | Weekly discovery of new skill repos — search, scan, add, publish  |
| `.github/workflows/submodule-update.yml`   | file | Weekly check for upstream submodule updates — create PR if found  |
| `.github/workflows/megalinter.yml`         | file | Lint on push/PR — markdown tables, YAML, JSON, spell check       |
| `.github/workflows/npm-publish.yml`        | file | Publish to npm on `v*` tags, create GitHub Release                |

## Key Symbols

### skill-discovery.yml

| Symbol              | Kind | Visibility | Location                                     | Purpose                                                          |
| ------------------- | ---- | ---------- | -------------------------------------------- | ---------------------------------------------------------------- |
| `discover`          | step | internal   | `.github/workflows/skill-discovery.yml:33`   | Searches GitHub for trending SKILL.md repos and top agent-skills repos |
| `evaluate`          | step | internal   | `.github/workflows/skill-discovery.yml:54`   | Security-scans candidates (eval/exec, credentials, executables, markdown ratio) |
| `Sync documentation`| step | internal  | `.github/workflows/skill-discovery.yml:162`  | Runs `sync-docs.js` to update counts                             |
| `Rebuild GH Pages`  | step | internal  | `.github/workflows/skill-discovery.yml:177`  | Runs `build-catalog.js` and commits                              |
| `Update Wiki`        | step | internal  | `.github/workflows/skill-discovery.yml:186`  | Inline Node.js script to update wiki                             |
| `Bump npm version`   | step | internal  | `.github/workflows/skill-discovery.yml:236`  | Patch version bump + tag if new sources were added               |
| `Create report issue`| step | internal  | `.github/workflows/skill-discovery.yml:246`  | Creates a discovery report issue with scan results               |

### submodule-update.yml

| Symbol                   | Kind | Visibility | Location                                      | Purpose                                            |
| ------------------------ | ---- | ---------- | --------------------------------------------- | -------------------------------------------------- |
| `check`                  | step | internal   | `.github/workflows/submodule-update.yml:34`   | Fetches all submodules, compares local vs remote HEAD |
| `Create PR`              | step | internal   | `.github/workflows/submodule-update.yml:85`   | Creates PR with update report table                 |

## Data Flow

```
Weekly cron (Monday 09:00 UTC)
    │
    ├──► skill-discovery.yml
    │    GitHub Search → Security Scan → git submodule add → sync-docs → build-catalog → wiki → npm bump → issue report
    │
    └──► submodule-update.yml
         git fetch per submodule → diff → create PR if updates found
```

## Configuration

| Variable/Secret  | Used by             | Purpose                         |
| ---------------- | ------------------- | ------------------------------- |
| `GITHUB_TOKEN`   | All workflows       | API access, push, PR creation   |
| `NPM_TOKEN`      | npm-publish.yml     | npm registry authentication     |

### Quality Gates (skill-discovery)

| Gate                    | Threshold   |
| ----------------------- | ----------- |
| Minimum stars           | 50          |
| Minimum SKILL.md files  | 3           |
| Minimum markdown ratio  | 30%         |
| No obfuscated code      | eval/exec/subprocess patterns |
| No hardcoded credentials| password/api_key/secret_key   |

## Inventory Notes

- **Coverage**: full
- **Notes**: All 4 workflows documented. The `skill-discovery.yml` is the most complex — it contains inline Node.js for wiki updates.
