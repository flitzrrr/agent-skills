# Contributing to Agent Skills Hub

Thanks for your interest in contributing.

## Adding a New Skill Source

1. Fork this repository
2. Add the source as a Git submodule:
   ```bash
   git submodule add https://github.com/owner/repo.git vendor/owner-repo
   ```
3. Create symlinks in `skills/` for each skill:
   ```bash
   ln -sf ../vendor/owner-repo/skill-name skills/prefix-skill-name
   ```
4. Run the doc sync:
   ```bash
   node bin/sync-docs.js
   ```
5. Update `README.md` sources table with the new entry
6. Open a Pull Request

## Quality Requirements

New sources must meet these criteria:

| Gate | Threshold |
|------|-----------|
| Minimum stars | 50 |
| Minimum SKILL.md files | 3 |
| Minimum markdown ratio | 30% |
| No obfuscated code | eval/exec/subprocess patterns |
| No hardcoded credentials | No passwords or API keys |
| Valid license | Must have an OSS license |

## Naming Convention

Skills are namespaced by source to avoid collisions. Use a lowercase prefix derived from the source name, followed by a hyphen:

```
skills/{prefix}-{skill-name}
```

Examples: `tob-static-analysis`, `cloudflare-wrangler`, `finance-equity-research`

## Reporting Issues

- Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template for problems
- Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template for suggestions\
- Use the [New Skill Source](.github/ISSUE_TEMPLATE/new_source.md) template to propose a new source

## Code Style

- No emojis in code or documentation
- Use standard markdown formatting
- Keep documentation concise
