---
type: documentation
entity: feature
feature: "auto-discovery"
version: 1.0
---

# Feature: Auto-Discovery

> Part of [Agent Skills Hub](../overview.md)

## Summary

Every Monday at 09:00 UTC, a GitHub Actions workflow automatically searches for trending AI agent skill repositories, security-scans them, and adds qualifying ones as new vendor submodules — complete with symlinks, catalog updates, wiki sync, and npm version bump.

## How It Works

### User Flow

1. No user action required — runs on a weekly cron schedule
2. A discovery report issue is created each week with scan results
3. If new sources are found, an npm patch version is published automatically

### Technical Flow

1. **Search**: GitHub API queries for repos with `SKILL.md` pushed in the last 7 days (sorted by stars) and repos tagged `agent-skills` (>100 stars)
2. **Deduplicate**: Merge results, remove repos already present as submodules
3. **Filter**: Skip repos with <3 SKILL.md files or <50 stars
4. **Security scan**: Clone each candidate and check:
   - Files with `eval`/`exec`/`subprocess` patterns (max 3 allowed)
   - JSON/env files with credential patterns (0 allowed)
   - Executable file count (noted if >5)
   - Markdown ratio (must be ≥30% of total files)
5. **Add**: `git submodule add` for passing repos, create symlinks in `skills/`
6. **Sync**: Run `sync-docs.js` and `build-catalog.js`
7. **Publish**: Update wiki, bump npm version, push tag, create report issue

## Implementation

| Module                           | Symbols               | Role                                      |
| -------------------------------- | --------------------- | ----------------------------------------- |
| [ci-cd](../modules/ci-cd.md)    | `discover` step       | GitHub API search for candidates          |
| [ci-cd](../modules/ci-cd.md)    | `evaluate` step       | Security scanning and submodule addition  |
| [build](../modules/build.md)    | `sync-docs.js`        | Updates counts in platform config files   |
| [build](../modules/build.md)    | `build-catalog.js`    | Rebuilds catalog.json                     |
| [build](../modules/build.md)    | `update-wiki.js`      | Pushes catalog to GitHub Wiki             |

## Configuration

- **Cron**: `0 9 * * 1` (Monday 09:00 UTC)
- **Can be triggered manually** via `workflow_dispatch`
- **Quality gates**: Configured inline in the workflow (stars, SKILL.md count, markdown ratio, security patterns)

## Edge Cases & Limitations

- **GitHub API rate limits**: Search queries may return incomplete results under heavy load
- **False positives in security scan**: `eval` in documentation files could cause false rejection
- **No removal**: The workflow only adds sources — it never removes deprecated or abandoned ones
- **Direct push to main**: Accepted sources are committed directly (not via PR), relying on the security scan as the gate

## Related Features

- [Vendor Sync](vendor-sync.md) — updates existing sources weekly
- [Catalog](catalog.md) — rebuilt after each discovery run
