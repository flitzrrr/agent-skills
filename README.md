# Agent Skills Hub

[![npm version](https://img.shields.io/npm/v/@flitzrrr/agent-skills?style=flat-square&color=cb3837)](https://www.npmjs.com/package/@flitzrrr/agent-skills)
[![Skills](https://img.shields.io/badge/skills-127-blue?style=flat-square)](skills/)
[![Sources](https://img.shields.io/badge/sources-15-green?style=flat-square)](vendor/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Weekly Discovery](https://img.shields.io/badge/auto--discovery-weekly-purple?style=flat-square)](.github/workflows/skill-discovery.yml)

A curated collection of **127 agent skills** from **15 industry-leading sources**, organized for flat access and compatible with all major AI coding assistants.

---

## Quick Install

**Ask your AI agent** — paste this into any AI coding assistant:

> Clone the agent-skills repository from https://github.com/flitzrrr/agent-skills with all submodules. Then symlink all skills from the `skills/` directory into my local agent skills directory. Preserve any existing skills I already have — do not overwrite them.

**Or use the CLI:**

```bash
npx @flitzrrr/agent-skills install
```

<details>
<summary>More CLI commands</summary>

| Command | Description |
|---------|-------------|
| `npx @flitzrrr/agent-skills install` | Install for all platforms |
| `npx @flitzrrr/agent-skills install antigravity` | Antigravity only |
| `npx @flitzrrr/agent-skills install codex` | Codex only |
| `npx @flitzrrr/agent-skills install opencode` | OpenCode only |
| `npx @flitzrrr/agent-skills update` | Pull latest skills |
| `npx @flitzrrr/agent-skills list` | List available skills |

</details>

<details>
<summary>Manual setup</summary>

```bash
git clone --recurse-submodules git@github.com:flitzrrr/agent-skills.git
cd agent-skills

# Symlink into your platform:
ln -sf $(pwd)/skills/* ~/.gemini/antigravity/skills/
ln -sf $(pwd)/skills/* ~/.codex/skills/
ln -sf $(pwd)/skills/* ~/.config/opencode/skills/

# Update later:
git submodule update --remote --merge
```

</details>

---

## Platform Support

| Platform | Config | Auto-Discovery |
|----------|--------|:--------------:|
| Claude Code | `CLAUDE.md` | Yes |
| Antigravity | `skills/` symlinks | — |
| Codex | `AGENTS.md` | Yes |
| OpenCode | `AGENTS.md` + `skills/` | — |
| Cursor | `.cursorrules` | Yes |
| Lovable | `.lovable` | Yes |
| Windsurf | `AGENTS.md` | Yes |
| Any agent | `SKILL.md` per skill | — |

---

## Sources

| Source | Skills | Focus | Added |
|--------|:------:|-------|-------|
| [getsentry/skills](https://github.com/getsentry/skills) | 24 | Security, code review, Git workflow, Django | 2026-03-14 |
| [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill) | 16 | SEO auditing | 2026-03-14 |
| [DasDigitaleMomentum/opencode-processing-skills](https://github.com/DasDigitaleMomentum/opencode-processing-skills) | 9 | Multi-session planning | 2026-03-14 |
| [anthropics/skills](https://github.com/anthropics/skills) | 17 | Document gen, creative design, MCP | 2026-03-14 |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 5 | React, Next.js, web design | 2026-03-14 |
| [trailofbits/skills](https://github.com/trailofbits/skills) | 30 | Security auditing, static analysis, smart contracts | 2026-03-14 |
| [cloudflare/skills](https://github.com/cloudflare/skills) | 9 | Workers, Durable Objects, MCP | 2026-03-14 |
| [stripe/ai](https://github.com/stripe/ai) | 2 | Stripe best practices | 2026-03-14 |
| [expo/skills](https://github.com/expo/skills) | 3 | Expo design and deployment | 2026-03-14 |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | 7 | Design-to-code, shadcn/ui, Remotion | 2026-03-14 |
| [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) | 3 | Terraform generation | 2026-03-14 |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | 1 | Postgres best practices | 2026-03-14 |
| [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills) | 5 | React Native, GitHub workflows | 2026-03-14 |
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | 100+ | Science, bioinformatics, ML, chemistry | 2026-03-14 |
| [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins) | 7 | Finance: IB, equity research, PE, wealth mgmt | 2026-03-14 |

New sources are discovered and added automatically every Monday via [GitHub Actions](.github/workflows/skill-discovery.yml). All candidates are security-scanned before integration.

---

## Repository Structure

```
agent-skills/
├── skills/          127 symlinks (flat access)
├── vendor/          15 Git submodules (upstream sources)
├── bin/cli.js       npx installer
├── AGENTS.md        Codex / OpenCode / Windsurf
├── CLAUDE.md        Claude Code
├── .cursorrules     Cursor
├── .lovable         Lovable
└── CHEATSHEET.md    Decision guide
```

---

## Naming Convention

Skills are namespaced by source to avoid collisions:

| Source | Prefix | Example |
|--------|--------|---------|
| Sentry | — | `code-review`, `security-review` |
| Anthropic | `anthropic-` | `anthropic-pdf`, `anthropic-mcp-builder` |
| Vercel | `vercel-` | `vercel-react-best-practices` |
| Trail of Bits | `tob-` | `tob-static-analysis` |
| Cloudflare | `cloudflare-` | `cloudflare-wrangler` |
| Google Stitch | `stitch-` | `stitch-shadcn-ui` |
| HashiCorp | `terraform-` | `terraform-code-generation` |
| Finance | `finance-` | `finance-equity-research` |
| Scientific | `scientific` | `scientific` (100+ sub-skills) |

---

## Automation

| Workflow | Schedule | What it does |
|----------|----------|-------------|
| [Skill Discovery](.github/workflows/skill-discovery.yml) | Weekly | Finds trending repos, security-scans, auto-adds |
| [npm Publish](.github/workflows/npm-publish.yml) | On tag `v*` | Publishes to npm + creates GitHub Release |
| [MegaLinter](.github/workflows/megalinter.yml) | On push/PR | Lints markdown, YAML, JSON |

---

## License

MIT — applies to the CLI, workflows, and documentation in this repository.
Each vendored submodule in `vendor/` retains its own original license.
