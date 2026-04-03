---
type: documentation
entity: project-overview
version: 1.0
---

# Agent Skills Hub

## Purpose

Agent Skills Hub is a curated collection of AI agent skills from multiple open-source repositories, organized for flat access and compatible with all major AI coding assistants (Claude Code, Codex, Cursor, Antigravity, OpenCode, Lovable, Windsurf). It solves the problem of fragmented skill sources by aggregating them into a single, installable package with consistent naming and a unified CLI.

## Architecture

The project follows a **vendor-symlink** architecture:

1. **Upstream sources** are tracked as Git submodules under `vendor/`
2. **Skills are exposed** as symlinks under `skills/`, providing flat access regardless of upstream directory structure. Some skills are local forks (real directories) for extensions not yet upstreamed.
3. **Platform config files** at the repo root (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.lovable`) and `.github/copilot-instructions.md` (VS Code) enable auto-discovery by each platform
4. **Build scripts** in `bin/` keep counts, catalogs, and platform configs in sync
5. **GitHub Actions** automate discovery of new sources, submodule updates, linting, npm publishing, and wiki updates
6. **Plans** in `plans/` track multi-phase implementation work using the `create-plan` / `update-plan` skill workflow

### System Diagram

```
┌──────────────────────────────────────────────────────────────┐
│  GitHub Actions (weekly)                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ skill-       │  │ submodule-   │  │ npm-publish      │   │
│  │ discovery    │  │ update       │  │ (on v* tag)      │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────────┘   │
│         │                 │                  │               │
│         ▼                 ▼                  ▼               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Repository                         │   │
│  │  vendor/          19 Git submodules (upstream)        │   │
│  │  skills/          symlinks → vendor/ + local forks     │   │
│  │  bin/             CLI + build scripts                 │   │
│  │  docs/            GitHub Pages catalog                │   │
│  │  .github/         CI workflows                        │   │
│  └──────────────────────────────────────────────────────┘   │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ npm package  │  │ GitHub Pages │  │ GitHub Wiki       │   │
│  │ (CLI)        │  │ (catalog)    │  │ (catalog mirror)  │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### Tech Stack

- **Runtime:** Node.js 20 (CLI and build scripts)
- **Package Manager:** npm (published as `@flitzrrr/agent-skills`)
- **CI:** GitHub Actions (MegaLinter, weekly discovery, submodule updates, npm publish)
- **Linting:** MegaLinter (documentation flavor) — markdown, YAML, JSON, spell check
- **Hosting:** GitHub Pages (searchable catalog), GitHub Wiki (catalog mirror)

## Modules

| Module | Description                                                  | Documentation                    |
| ------ | ------------------------------------------------------------ | -------------------------------- |
| cli    | npm CLI for installing/updating skills across platforms       | [Detail](modules/cli.md)        |
| build  | Scripts to sync counts, build catalog, and update wiki       | [Detail](modules/build.md)      |
| ci-cd  | GitHub Actions workflows for automation                      | [Detail](modules/ci-cd.md)      |
| skills | Skill collection — symlinks to vendor + custom skills        | [Detail](modules/skills.md)     |

## Key Features

| Feature         | Description                                                          | Documentation                              |
| --------------- | -------------------------------------------------------------------- | ------------------------------------------ |
| Installation    | Multi-platform skill installation via CLI or manual symlinks         | [Detail](features/installation.md)         |
| Auto-Discovery  | Weekly automated discovery and security-scanning of new skill repos  | [Detail](features/auto-discovery.md)       |
| Catalog         | Searchable GitHub Pages site and Wiki with all skills                | [Detail](features/catalog.md)              |
| Vendor Sync     | Automated weekly submodule updates via PR                            | [Detail](features/vendor-sync.md)          |
| l4l Integration | MCP execution backend for execute-work-package (multi-transport)     | See [l4l repo](https://github.com/flitzrrr/l4l) |

## Development

### Setup

```bash
git clone --recurse-submodules git@github.com:flitzrrr/agent-skills.git
cd agent-skills
```

No `npm install` needed — all scripts use Node.js stdlib only.

### Build & Run

```bash
# Rebuild catalog.json from SKILL.md frontmatter
node bin/build-catalog.js

# Sync skill/source counts across README, AGENTS.md, CLAUDE.md, etc.
node bin/sync-docs.js

# Update GitHub Wiki (requires SSH access)
node bin/update-wiki.js
```

### Testing

```bash
# Run CLI tests (syntax checks + functional tests)
node bin/test-cli.js

# Or via npm
npm test
```

## References

- npm package: [@flitzrrr/agent-skills](https://www.npmjs.com/package/@flitzrrr/agent-skills)
- GitHub Pages catalog: https://flitzrrr.github.io/agent-skills/
- GitHub Wiki: https://github.com/flitzrrr/agent-skills/wiki
