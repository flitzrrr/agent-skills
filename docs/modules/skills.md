---
type: documentation
entity: module
module: "skills"
version: 1.0
---

# Module: skills

> Part of [Agent Skills Hub](../overview.md)

## Overview

### Responsibility

The skills module is the core of the repository — it contains the actual skill collection. Most skills are symlinks pointing into `vendor/` submodules; a few are custom, first-party skills with their own code.

IS responsible for: providing flat, consistent access to all skills via `skills/<name>/SKILL.md`.
IS NOT responsible for: upstream skill content (vendor module), installation (cli module), or discovery (ci-cd module).

### Dependencies

| Dependency | Type     | Purpose                                          |
| ---------- | -------- | ------------------------------------------------ |
| `vendor/`  | internal | Git submodules that contain the actual skill files|

## Structure

| Path                                       | Type    | Purpose                                                     |
| ------------------------------------------ | ------- | ----------------------------------------------------------- |
| `skills/`                                  | dir     | Root directory — ~503 entries, mostly symlinks               |
| `skills/<name> → ../vendor/<source>/...`   | symlink | Symlink to upstream skill in a vendor submodule              |
| `skills/product-description-seo/`          | dir     | Custom first-party skill — SEO product descriptions          |
| `skills/dispatch-parallel-agents/`         | dir     | Custom first-party skill — parallel subagent dispatch        |
| `skills/systematic-debugging/`             | dir     | Custom first-party skill — root-cause debugging workflow     |
| `skills/tob-gh-cli/`                       | dir     | Custom first-party skill — GitHub CLI automation             |

### Vendor Sources (19 submodules)

| Vendor directory                    | Source                                | Skill prefix     |
| ----------------------------------- | ------------------------------------- | ---------------- |
| `vendor/getsentry-skills`           | getsentry/skills                      | (none)           |
| `vendor/agentic-seo-skill`          | Bhanunamikaze/Agentic-SEO-Skill       | `seo`            |
| `vendor/opencode-processing-skills` | DasDigitaleMomentum/opencode-...      | (none)           |
| `vendor/anthropic-skills`           | anthropics/skills                     | `anthropic-`     |
| `vendor/vercel-agent-skills`        | vercel-labs/agent-skills              | `vercel-`        |
| `vendor/trailofbits-skills`         | trailofbits/skills                    | `tob-`           |
| `vendor/cloudflare-skills`          | cloudflare/skills                     | `cloudflare-`    |
| `vendor/stripe-skills`              | stripe/ai                             | `stripe-`        |
| `vendor/expo-skills`                | expo/skills                           | `expo-`          |
| `vendor/google-stitch-skills`       | google-labs-code/stitch-skills        | `stitch-`        |
| `vendor/hashicorp-skills`           | hashicorp/agent-skills                | `terraform-`     |
| `vendor/supabase-skills`            | supabase/agent-skills                 | `supabase-`      |
| `vendor/callstack-skills`           | callstackincubator/agent-skills       | `callstack-`     |
| `vendor/scientific-skills`          | K-Dense-AI/claude-scientific-skills   | `scientific`     |
| `vendor/anthropic-finance`          | anthropics/financial-services-plugins | `finance-`       |
| `vendor/marketingskills`            | coreyhaines31/marketingskills         | (none)           |
| `vendor/itsmostafa-aws-agent-skills`| itsmostafa/aws-agent-skills           | `aws-`           |
| `vendor/MoizIbnYousaf-Ai-Agent-Skills`| MoizIbnYousaf/Ai-Agent-Skills       | (varies)         |
| `vendor/JackyST0-awesome-agent-skills`| JackyST0/awesome-agent-skills       | (varies)         |

### Custom Skills

| Skill                     | Description                                                  | Contents                              |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------- |
| `product-description-seo` | E2E workflow for SEO product descriptions (9 phases)          | SKILL.md, KEYWORDS.md, CROSS-SELL.md, 6 Python scripts |
| `dispatch-parallel-agents`| Dispatch independent tasks to parallel subagents              | skill.md                              |
| `systematic-debugging`    | Root-cause analysis debugging workflow                        | skill.md                              |
| `tob-gh-cli`              | GitHub CLI automation patterns                                | SKILL.md                              |

## Key Symbols

Skills are not code — they are instruction documents (SKILL.md). The only skill with executable code is `product-description-seo`:

| Symbol             | Kind   | Visibility | Location                                                  | Purpose                                           |
| ------------------ | ------ | ---------- | --------------------------------------------------------- | ------------------------------------------------- |
| `analyze_catalog`  | script | public     | `skills/product-description-seo/scripts/analyze_catalog.py` | Analyze catalog for thin descriptions             |
| `track_progress`   | script | public     | `skills/product-description-seo/scripts/track_progress.py`  | Track description update campaign progress        |
| `extract_category` | script | public     | `skills/product-description-seo/scripts/extract_category.py`| Extract category products for batch prompting     |
| `check_quality`    | script | public     | `skills/product-description-seo/scripts/check_quality.py`   | QA check against 8 SEO criteria                   |
| `update_catalog`   | script | public     | `skills/product-description-seo/scripts/update_catalog.py`  | Write descriptions back to catalog with backup    |
| `validate_json`    | script | public     | `skills/product-description-seo/scripts/validate_json.py`   | Validate JSON structure after updates             |

## Data Flow

```
vendor/<source>/skills/<name>/SKILL.md
    │
    │  symlink
    ▼
skills/<prefix>-<name>/SKILL.md
    │
    │  read by agent
    ▼
Agent follows SKILL.md instructions
```

## Configuration

- **Naming convention**: Skills are namespaced by source prefix to avoid collisions (e.g., `anthropic-pdf`, `tob-static-analysis`)
- **Platform configs**: `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.lovable` at repo root list available skill categories for auto-discovery

## Inventory Notes

- **Coverage**: best-effort
- **Notes**: Only custom (first-party) skills are inventoried in detail. Vendor skills are tracked by source; their content is documented upstream.
