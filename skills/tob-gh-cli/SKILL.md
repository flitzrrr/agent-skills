---
name: gh-cli
description: Intercepts GitHub URL fetches and redirects to the authenticated `gh` CLI. Use when Claude tries to access GitHub via WebFetch or curl/wget, when you see 404 errors on private repos, when hitting GitHub API rate limits, or when GitHub API responses are incomplete. Provides hooks that automatically suggest the correct `gh` CLI command for any GitHub URL access pattern.
---

# GitHub CLI Integration

A plugin that intercepts GitHub URL fetches and redirects Claude to use the authenticated `gh` CLI instead.

## Problem

Claude Code's `WebFetch` tool and Bash `curl`/`wget` commands don't use the user's GitHub authentication. This means:

- **Private repos**: Fetches fail with 404 errors
- **Rate limits**: Unauthenticated requests are limited to 60/hour (vs 5,000/hour authenticated)
- **Missing data**: Some API responses are incomplete without authentication

## Solution

This plugin provides PreToolUse hooks that intercept GitHub URL access via `WebFetch` or `curl`/`wget`, and suggest the correct `gh` CLI command.

### What Gets Intercepted

| Tool | Pattern | Suggestion |
|------|---------|------------|
| `WebFetch` | `github.com/{owner}/{repo}` | `gh repo view owner/repo` |
| `WebFetch` | `github.com/.../blob/...` | `gh repo clone` + Read |
| `WebFetch` | `github.com/.../tree/...` | `gh repo clone` + Read/Glob/Grep |
| `WebFetch` | `api.github.com/repos/.../pulls` | `gh pr list` / `gh pr view` |
| `WebFetch` | `api.github.com/repos/.../issues` | `gh issue list` / `gh issue view` |
| `WebFetch` | `api.github.com/...` | `gh api <endpoint>` |
| `WebFetch` | `raw.githubusercontent.com/...` | `gh repo clone` + Read |
| `Bash` | `curl https://api.github.com/...` | `gh api <endpoint>` |
| `Bash` | `curl https://raw.githubusercontent.com/...` | `gh repo clone` + Read |
| `Bash` | `wget https://github.com/...` | `gh release download` |

### What Passes Through

- Non-GitHub URLs
- GitHub Pages sites (`*.github.io`)
- Commands already using `gh` (except anti-patterns)
- Git commands (`git clone`, `git push`, etc.)
- Search commands that mention GitHub URLs (`grep`, `rg`, etc.)

## Prerequisites

- [GitHub CLI (`gh`)](https://cli.github.com/) must be installed and authenticated (`gh auth login`)
- If `gh` is not installed, the hooks pass through without disruption

## Usage

This skill operates automatically via hooks. No manual invocation required. When you attempt to access GitHub URLs, the hooks will intercept and suggest the authenticated alternative.

### Common gh CLI Commands

```bash
# View repo info
gh repo view owner/repo

# List PRs
gh pr list --repo owner/repo

# View a specific PR
gh pr view 123 --repo owner/repo

# API access
gh api repos/owner/repo/pulls

# Clone a repo
gh repo clone owner/repo
```
