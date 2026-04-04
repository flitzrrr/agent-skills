# Agent Skills Hub

[![npm version](https://img.shields.io/npm/v/@flitzrrr/agent-skills?style=flat-square&color=cb3837)](https://www.npmjs.com/package/@flitzrrr/agent-skills)
[![npm downloads](https://img.shields.io/npm/dm/@flitzrrr/agent-skills?style=flat-square)](https://www.npmjs.com/package/@flitzrrr/agent-skills)
[![Skills](https://img.shields.io/badge/skills-504-blue?style=flat-square)](skills/)
[![Sources](https://img.shields.io/badge/sources-19-green?style=flat-square)](vendor/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Weekly Discovery](https://img.shields.io/badge/auto--discovery-weekly-purple?style=flat-square)](.github/workflows/skill-discovery.yml)

**504 agent skills** from **19 sources**, flat-access, works with Claude Code, Codex, Cursor, Antigravity, OpenCode, Lovable, and Windsurf.

[Browse the full catalog](https://flitzrrr.github.io/agent-skills/) | [Decision guide](CHEATSHEET.md)

---

## Install

```bash
npx @flitzrrr/agent-skills install
```

Installs for all detected platforms. Target a specific one with `install codex`, `install antigravity`, or `install opencode`.

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

<details>
<summary>All CLI commands</summary>

| Command                                       | Description              |
| --------------------------------------------- | ------------------------ |
| `npx @flitzrrr/agent-skills install`          | Install for all platforms|
| `npx @flitzrrr/agent-skills install <target>` | Install for one platform |
| `npx @flitzrrr/agent-skills update`           | Pull latest skills       |
| `npx @flitzrrr/agent-skills list`             | List available skills    |

</details>

---

## Platform Support

| Platform    | Config                 | Auto-Discovery |
| ----------- | ---------------------- | :------------: |
| Claude Code | `CLAUDE.md`            | Yes            |
| Codex       | `AGENTS.md`            | Yes            |
| Cursor      | `.cursorrules`         | Yes            |
| Lovable     | `.lovable`             | Yes            |
| Windsurf    | `AGENTS.md`            | Yes            |
| Antigravity | `skills/` symlinks     | --             |
| OpenCode    | `AGENTS.md` + `skills/`| --             |
| Any agent   | `SKILL.md` per skill   | --             |

---

## Sources

| Source                                                                                           | Skills | Focus                                              |
| ------------------------------------------------------------------------------------------------ | -----: | -------------------------------------------------- |
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)    |    175 | Science, bioinformatics, ML, chemistry             |
| [trailofbits/skills](https://github.com/trailofbits/skills)                                     |     60 | Security auditing, static analysis, smart contracts|
| [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins)|     56 | Finance: IB, equity research, PE, wealth mgmt      |
| [MoizIbnYousaf/Ai-Agent-Skills](https://github.com/MoizIbnYousaf/Ai-Agent-Skills)               |     48 | Database design, debugging, code patterns          |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)                |     33 | Marketing: SEO, email, content, analytics          |
| [getsentry/skills](https://github.com/getsentry/skills)                                         |     24 | Security, code review, Git workflow, Django        |
| [itsmostafa/aws-agent-skills](https://github.com/itsmostafa/aws-agent-skills)                    |     18 | AWS infrastructure and services                    |
| [anthropics/skills](https://github.com/anthropics/skills)                                        |     17 | Document gen, creative design, MCP                 |
| [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills)                              |     14 | Terraform generation                               |
| [expo/skills](https://github.com/expo/skills)                                                    |     11 | Expo design and deployment                         |
| [cloudflare/skills](https://github.com/cloudflare/skills)                                        |      9 | Workers, Durable Objects, MCP                      |
| [DasDigitaleMomentum/opencode-processing-skills](https://github.com/DasDigitaleMomentum/opencode-processing-skills) | 9 | Multi-session planning                 |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills)              |      7 | Design-to-code, shadcn/ui, Remotion                |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)                          |      5 | React, Next.js, web design                         |
| [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills)            |      5 | React Native, GitHub workflows                     |
| [JackyST0/awesome-agent-skills](https://github.com/JackyST0/awesome-agent-skills)                |      5 | General-purpose agent patterns                     |
| [stripe/ai](https://github.com/stripe/ai)                                                        |      2 | Stripe best practices                              |
| [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill)           |      1 | SEO auditing (16 sub-skills in one SKILL.md)       |
| [supabase/agent-skills](https://github.com/supabase/agent-skills)                                |      1 | Postgres best practices                            |

New sources are discovered weekly via [GitHub Actions](.github/workflows/skill-discovery.yml). All candidates are security-scanned before integration.

---

## Repository Structure

```
agent-skills/
  skills/          504 entries (symlinks + local forks, flat access to all skills)
  vendor/          19 Git submodules (upstream sources)
  bin/              CLI + build scripts (catalog, sync, wiki)
  docs/             GitHub Pages catalog + project documentation
  .github/          CI workflows (discovery, linting, publishing, submodule sync)
  CLAUDE.md         Claude Code config
  AGENTS.md         Codex / OpenCode / Windsurf config
  CHEATSHEET.md     Which skill to use when
  .cursorrules      Cursor config
  .lovable          Lovable config
```

---

## Naming Convention

Skills are namespaced by source to avoid collisions:

| Source        | Prefix         | Example                           |
| ------------- | -------------- | --------------------------------- |
| Sentry        | --             | `code-review`, `security-review`  |
| Anthropic     | `anthropic-`   | `anthropic-pdf`                   |
| Vercel        | `vercel-`      | `vercel-react-best-practices`     |
| Trail of Bits | `tob-`         | `tob-static-analysis`             |
| Cloudflare    | `cloudflare-`  | `cloudflare-wrangler`             |
| Google Stitch | `stitch-`      | `stitch-shadcn-ui`                |
| HashiCorp     | `terraform-`   | `terraform-code-generation`       |
| Finance       | `finance-`     | `finance-equity-research`         |
| Scientific    | `scientific-`  | `scientific-bioinformatics`       |
| Marketing     | --             | `content-strategy`, `seo-audit`   |
| AWS           | `aws-`         | `aws-lambda`                      |
| Callstack     | `callstack-`   | `callstack-react-native-best-practices` |

---

## Automation

| Workflow                                                              | Trigger     | What it does                                    |
| --------------------------------------------------------------------- | ----------- | ----------------------------------------------- |
| [Skill Discovery](.github/workflows/skill-discovery.yml)             | Weekly      | Finds trending repos, security-scans, auto-adds |
| [Submodule Update](.github/workflows/submodule-update.yml)           | Weekly      | Pulls upstream changes, creates PR              |
| [MegaLinter](.github/workflows/megalinter.yml)                       | Push / PR   | Lints markdown, YAML, JSON                      |
| [npm Publish](.github/workflows/npm-publish.yml)                     | Tag `v*`    | Publishes to npm, creates GitHub Release        |

---

## l4l -- MCP Execution Backend

The [execute-work-package](skills/execute-work-package) skill uses [l4l](https://github.com/flitzrrr/l4l) as its default MCP execution backend. l4l exposes 5 MCP tools (`precheck_new`, `precheck_iterate`, `approve_blueprint`, `execute`, `handle_report`) that implement the gated precheck-approve-execute lifecycle. When l4l MCP tools are available, the skill uses them automatically (Option A); fresh-agent and stateful transports are documented fallbacks. See the [l4l Claude Code setup guide](https://github.com/flitzrrr/l4l/blob/main/docs/CLAUDE_CODE_SETUP.md) for configuration instructions.

---

## License

MIT -- applies to the CLI, workflows, and documentation in this repository.
Each vendored submodule in `vendor/` retains its own original license.
