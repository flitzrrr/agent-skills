---
type: documentation
entity: feature
feature: "installation"
version: 1.0
---

# Feature: Installation

> Part of [Agent Skills Hub](../overview.md)

## Summary

Multi-platform skill installation that creates symlinks from a central repository clone into each AI coding assistant's skill directory. Supports VS Code (GitHub Copilot), Claude Code, Codex, Antigravity (Gemini), OpenCode, and Cursor.

## How It Works

### User Flow

1. User runs `npx @flitzrrr/agent-skills install` (or `install <platform>`)
2. CLI clones the full repository (with submodules) to `~/.agent-skills/`
3. For each platform, symlinks are created from `~/.agent-skills/skills/*` into the platform's skill directory
4. Existing skills are preserved — no overwrite
5. User can update later with `npx @flitzrrr/agent-skills update`

### Technical Flow

1. `cloneRepo()` runs `git clone --recurse-submodules` to `~/.agent-skills/` (or `git pull` if exists)
2. For each platform in `PLATFORMS`, `installForPlatform()`:
   - Creates the platform's skill directory if missing (`fs.mkdirSync`)
   - Iterates `~/.agent-skills/skills/` entries
   - For each entry not already present in target, creates a symlink (`fs.symlinkSync`)
3. Reports count of added vs skipped skills

## Implementation

| Module                           | Symbols            | Role                                     |
| -------------------------------- | ------------------ | ---------------------------------------- |
| [cli](../modules/cli.md)        | `cloneRepo`        | Clones or updates the repo               |
| [cli](../modules/cli.md)        | `installForPlatform` | Creates symlinks per platform          |
| [cli](../modules/cli.md)        | `PLATFORMS`        | Platform config (name, directory, notes)  |

## Configuration

| Platform     | Skill directory                          | Notes                               |
| ------------ | ---------------------------------------- | ----------------------------------- |
| VS Code      | `~/.copilot/skills/`                     | Symlinks created, copilot-instructions.md|
| Claude Code  | (project-level, no symlinks)             | CLAUDE.md auto-discovery            |
| Antigravity  | `~/.gemini/antigravity/skills/`          | Symlinks created                    |
| Codex        | `~/.codex/skills/`                       | Symlinks created                    |
| OpenCode     | `~/.config/opencode/skills/`             | Symlinks created                    |
| Cursor       | (workspace-level, no symlinks)           | .cursorrules auto-loaded            |

## Edge Cases & Limitations

- **Windows**: Uses `junction` symlinks, which require admin privileges on some Windows versions
- **Claude Code / Cursor**: Cannot use symlinks — require cloning repo into the project workspace
- **No uninstall command**: Removal is manual (delete symlinks and `~/.agent-skills/`)
- **No selective install**: All skills are installed; there is no per-skill selection

## Related Features

- [Vendor Sync](vendor-sync.md) — keeps upstream sources up to date
- [Auto-Discovery](auto-discovery.md) — adds new sources automatically
