# 🧠 Agent Skills Hub

> **128 AI agent skills** from **16 industry-leading sources** — organized, evaluated, and **multiplatform-ready** for all major AI coding IDEs.

## ✅ Supported Platforms

| Platform | Config File | Setup |
|----------|------------|-------|
| **Claude Code** | `CLAUDE.md` | Clone repo, skills auto-discovered |
| **Antigravity** | `skills/` dir | Symlink `skills/` into agent skill dir |
| **Codex** (OpenAI) | `AGENTS.md` | Clone repo, `AGENTS.md` auto-loaded |
| **OpenCode** | `AGENTS.md` + `skills/` | Clone repo, reference skills in prompts |
| **Cursor** | `.cursorrules` | Clone repo into workspace, rules auto-loaded |
| **Lovable** | `.lovable` | Add as project dependency |
| **Windsurf** | `AGENTS.md` | Clone repo, reference skill paths |
| **Generic Agent** | `SKILL.md` per skill | Read `skills/<name>/SKILL.md` |

## Sources (16)

| # | Source | Skills | Focus |
|---|--------|--------|-------|
| 1 | [getsentry/skills](https://github.com/getsentry/skills) | 24 | Security, code review, Git workflow, Django |
| 2 | [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill) | 16 | Comprehensive SEO auditing |
| 3 | [DasDigitaleMomentum/opencode-processing-skills](https://github.com/DasDigitaleMomentum/opencode-processing-skills) | 9 | Multi-session planning & docs |
| 4 | [anthropics/skills](https://github.com/anthropics/skills) | 17 | Document gen, creative design, MCP, API |
| 5 | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 5 | React/Next.js, web design, deployment |
| 6 | [trailofbits/skills](https://github.com/trailofbits/skills) | 30 | Advanced security auditing, static analysis, smart contracts |
| 7 | [cloudflare/skills](https://github.com/cloudflare/skills) | 9 | Workers, Durable Objects, MCP, web perf |
| 8 | [stripe/ai](https://github.com/stripe/ai) | 2 | Stripe best practices & SDK upgrades |
| 9 | [expo/skills](https://github.com/expo/skills) | 3 | Expo app design, deployment, upgrades |
| 10 | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | 7 | Design-to-code, shadcn/ui, Remotion |
| 11 | [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) | 3 | Terraform code/module/provider generation |
| 12 | [supabase/agent-skills](https://github.com/supabase/agent-skills) | 1 | Postgres best practices |
| 13 | [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills) | 5 | React Native, GitHub workflows |
| 14 | [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | 100+ | Science, bioinformatics, ML, chemistry |
| 15 | [ComposioHQ/skills](https://github.com/ComposioHQ/skills) | 1 | Connect agents to 1000+ external apps |
| 16 | [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins) | 7 | Finance: IB, equity research, PE, wealth mgmt |

## Repository Structure

```
agent-skills/
├── skills/               ← 128 symlinks (flat access to all skills)
├── vendor/               ← 16 Git submodules (upstream sources)
├── AGENTS.md             ← Codex / OpenCode / Windsurf
├── CLAUDE.md             ← Claude Code
├── .cursorrules          ← Cursor IDE
├── .lovable              ← Lovable AI
├── CHEATSHEET.md         ← Decision guide: which skill when
└── README.md             ← This file
```

## 🚀 Quick Install

### Option 1: Ask Your AI Agent (Copy-Paste Prompt)

Paste this into **any AI coding assistant** (Claude Code, Antigravity, Codex, Cursor, etc.):

> Clone the agent-skills repository from https://github.com/flitzrrr/agent-skills with all submodules. Then symlink all skills from the `skills/` directory into my local agent skills directory. Preserve any existing skills I already have — do not overwrite them.

### Option 2: npm CLI

```bash
npx @flitzrrr/agent-skills install              # Install for all platforms
npx @flitzrrr/agent-skills install antigravity   # Antigravity only
npx @flitzrrr/agent-skills install codex         # Codex only
npx @flitzrrr/agent-skills install opencode      # OpenCode only
npx @flitzrrr/agent-skills update                # Update all skills
npx @flitzrrr/agent-skills list                  # List available skills
```

### Option 3: Manual Setup

```bash
# Clone with all submodules
git clone --recurse-submodules git@github.com:flitzrrr/agent-skills.git
cd agent-skills

# Symlink skills into your platform (pick one or more):
ln -sf $(pwd)/skills/* ~/.gemini/antigravity/skills/   # Antigravity
ln -sf $(pwd)/skills/* ~/.codex/skills/                # Codex
ln -sf $(pwd)/skills/* ~/.config/opencode/skills/      # OpenCode

# Update all upstream sources later:
git submodule update --remote --merge
```

### Platform Auto-Discovery

Some platforms don't need symlinks — just clone the repo:

| Platform | How It Works |
|----------|-------------|
| **Claude Code** | Clone into project → `CLAUDE.md` auto-discovered |
| **Codex** | Clone into project → `AGENTS.md` auto-discovered |
| **Cursor** | Clone into workspace → `.cursorrules` auto-loaded |
| **Lovable** | `git submodule add` → `.lovable` auto-loaded |
| **Windsurf** | Clone into project → `AGENTS.md` auto-discovered |

## Naming Convention

| Source | Prefix | Example |
|--------|--------|---------|
| Sentry | *(none)* | `code-review`, `security-review` |
| SEO | `seo` | `seo` |
| OpenCode | *(none)* | `create-plan`, `resume-plan` |
| Anthropic | `anthropic-` | `anthropic-pdf`, `anthropic-mcp-builder` |
| Vercel | `vercel-` | `vercel-react-best-practices` |
| Trail of Bits | `tob-` | `tob-static-analysis`, `tob-semgrep-rule-creator` |
| Cloudflare | `cloudflare-` | `cloudflare-wrangler`, `cloudflare-web-perf` |
| Stripe | `stripe-` | `stripe-stripe-best-practices` |
| Expo | `expo` | `expo` |
| Google Stitch | `stitch-` | `stitch-shadcn-ui`, `stitch-remotion` |
| HashiCorp | `terraform-` | `terraform-code-generation` |
| Supabase | `supabase-` | `supabase-postgres` |
| CallStack | `callstack-` | `callstack-react-native-best-practices` |
| Scientific | `scientific` | `scientific` (100+ sub-skills) |
| Composio | `composio` | `composio` |
| Finance | `finance-` | `finance-equity-research`, `finance-private-equity` |

## License

Each vendored repository retains its original license. See individual repos for details.
