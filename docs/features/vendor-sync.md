---
type: documentation
entity: feature
feature: "vendor-sync"
version: 1.0
---

# Feature: Vendor Sync

> Part of [Agent Skills Hub](../overview.md)

## Summary

A weekly GitHub Actions workflow that checks all 19 vendor submodules for upstream updates and creates a pull request if any are found, including a detailed report of what changed.

## How It Works

### User Flow

1. No user action required — runs every Monday at 08:00 UTC
2. If updates are found, a PR is created with a table showing which submodules changed and how many commits are new
3. Maintainer reviews and merges the PR

### Technical Flow

1. Workflow checks out repo with all submodules (`submodules: recursive`)
2. For each `vendor/*/` directory:
   - `git fetch origin` to get latest remote state
   - Compare `HEAD` (local) vs `origin/main` or `origin/master`
   - If different: pull latest, record update details
3. If any updates found:
   - Stage all `vendor/` changes
   - Create branch `chore/auto-update-submodules-YYYY-MM-DD`
   - Commit with list of updated submodules
   - Create PR with a markdown table (submodule, status, commit count, latest commit)

## Implementation

| Module                           | Symbols        | Role                                            |
| -------------------------------- | -------------- | ----------------------------------------------- |
| [ci-cd](../modules/ci-cd.md)    | `check` step   | Fetches and compares each submodule             |
| [ci-cd](../modules/ci-cd.md)    | `Create PR` step | Creates branch + PR with update report        |

## Configuration

- **Cron**: `0 8 * * 1` (Monday 08:00 UTC — 1 hour before skill-discovery)
- **Can be triggered manually** via `workflow_dispatch`
- **Branch naming**: `chore/auto-update-submodules-YYYY-MM-DD`
- **Requires**: `GITHUB_TOKEN` for push and PR creation

## Edge Cases & Limitations

- **Default branch detection**: Tries `origin/main` first, falls back to `origin/master`. Repos with non-standard default branches (e.g., `develop`) will not be updated
- **No conflict resolution**: If a submodule update conflicts with local changes, the workflow will fail
- **PR-based**: Updates are not pushed directly — they require manual merge, adding a review gate
- **Stale PRs**: If previous update PRs are not merged, new ones will be created alongside them
- **Local fork exclusions**: `bin/sync-skills.sh` excludes locally forked skills (e.g., `execute-work-package`) to prevent overwriting transport extensions not yet upstreamed

## Related Features

- [Auto-Discovery](auto-discovery.md) — adds entirely new sources (vs. updating existing ones)
- [Catalog](catalog.md) — catalog should be rebuilt after merging submodule updates
