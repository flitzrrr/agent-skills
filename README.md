# 🧠 Agent Skills Hub

> A curated collection of **55 AI agent skills** from 5 industry-leading sources — organized, evaluated, and **multiplatform-ready** for all major AI coding IDEs.

## ✅ Supported Platforms

| Platform | Config File | Setup |
|----------|------------|-------|
| **Claude Code** | `CLAUDE.md` | Clone repo, skills auto-discovered |
| **Antigravity** | `skills/` dir | Symlink `skills/` into `~/.gemini/antigravity/skills/` |
| **Codex** (OpenAI) | `AGENTS.md` | Clone repo, `AGENTS.md` auto-loaded |
| **OpenCode** | `AGENTS.md` + `skills/` | Clone repo, reference skills in prompts |
| **Cursor** | `.cursorrules` | Clone repo into workspace, rules auto-loaded |
| **Lovable** | `.lovable` | Add as project dependency |
| **Windsurf** | `AGENTS.md` | Clone repo, reference skill paths |
| **Generic Agent** | `SKILL.md` per skill | Read `skills/<name>/SKILL.md` |

## Sources

| Source | Skills | Focus |
|--------|--------|-------|
| [getsentry/skills](https://github.com/getsentry/skills) | 24 | Security, code review, Git workflow, Django |
| [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill) | 16 sub-skills | Comprehensive SEO auditing |
| [DasDigitaleMomentum/opencode-processing-skills](https://github.com/DasDigitaleMomentum/opencode-processing-skills) | 9 | Multi-session planning & documentation |
| [anthropics/skills](https://github.com/anthropics/skills) | 17 | Document gen, creative design, MCP, API |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 5 | React/Next.js, web design, deployment |

## Repository Structure

```
agent-skills/
├── skills/               ← 55 symlinks (flat access to all skills)
├── vendor/               ← 5 Git submodules (upstream sources)
│   ├── getsentry-skills/
│   ├── agentic-seo-skill/
│   ├── opencode-processing-skills/
│   ├── anthropic-skills/
│   └── vercel-agent-skills/
├── AGENTS.md             ← Codex / OpenCode / Windsurf / generic agents
├── CLAUDE.md             ← Claude Code
├── .cursorrules          ← Cursor IDE
├── .lovable              ← Lovable AI
├── CHEATSHEET.md         ← Decision guide: which skill when
└── README.md             ← This file
```

## Quick Start

```bash
# Clone with all submodules
git clone --recurse-submodules git@github.com:flitzrrr/agent-skills.git

# Update all upstream sources
git submodule update --remote --merge
```

## Platform Setup

### Claude Code
```bash
# Option A: Add as plugin marketplace
/plugin marketplace add flitzrrr/agent-skills

# Option B: Clone into project, CLAUDE.md auto-loaded
git clone --recurse-submodules git@github.com:flitzrrr/agent-skills.git
```

### Antigravity (Gemini)
```bash
# Symlink skills into Antigravity's skill directory
ln -sf /path/to/agent-skills/skills/* ~/.gemini/antigravity/skills/
```

### Codex (OpenAI)
```bash
# Clone into workspace — AGENTS.md is auto-discovered
git clone --recurse-submodules git@github.com:flitzrrr/agent-skills.git
```

### Cursor
```bash
# Clone into workspace — .cursorrules auto-loaded
git clone --recurse-submodules git@github.com:flitzrrr/agent-skills.git
```

### Lovable
```bash
# Add as submodule to your Lovable project
git submodule add git@github.com:flitzrrr/agent-skills.git skills
```

### OpenCode / Windsurf / Generic
```bash
# Clone and reference skills/<name>/SKILL.md in your agent prompts
git clone --recurse-submodules git@github.com:flitzrrr/agent-skills.git
```

## Naming Convention

Skills are namespaced by source to avoid collisions:

| Source | Prefix | Example |
|--------|--------|---------|
| Sentry | *(none)* | `code-review`, `security-review` |
| Agentic SEO | `seo` | `seo` (single entry point) |
| OpenCode | *(none)* | `create-plan`, `resume-plan` |
| Anthropic | `anthropic-` | `anthropic-pdf`, `anthropic-mcp-builder` |
| Vercel | `vercel-` | `vercel-react-best-practices` |

## License

Each vendored repository retains its original license. See individual repos for details.
