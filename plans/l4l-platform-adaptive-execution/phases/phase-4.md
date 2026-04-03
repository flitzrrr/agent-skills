---
type: planning
entity: phase
plan: "l4l-platform-adaptive-execution"
phase: 4
status: completed
created: "2026-04-03"
updated: "2026-04-04"
---

# Phase 4: E2E Integration & Docs

> Part of [l4l-platform-adaptive-execution](../plan.md)

## Objective

Validate the full pipeline end-to-end (Claude Code → l4l MCP → precheck → gate → execute → digest) and document the setup for users of each platform.

## Scope

### Includes

- E2E test: Claude Code invokes l4l MCP tools to execute a real work package
- E2E test: Use realworld testbed (chimera_project or phoenix_project)
- l4l README update: skill-integration workflow, quick start for CC users
- agent-skills README update: mention l4l as MCP execution backend
- Troubleshooting guide for common issues (MCP connection, model config, scope errors)

### Excludes (deferred)

- Automated CI for E2E tests (manual validation is sufficient for now)
- Performance benchmarking
- Multi-model comparison (which Sub-LLM works best)

## Prerequisites

- [ ] Phase 3 completed (skill updated with Transport section)
- [ ] l4l server running locally with MCP enabled
- [ ] Claude Code with MCP server configuration pointing to l4l

## Deliverables

- [ ] E2E run log: CC → l4l MCP → work package execution (captured as session transcript)
- [ ] l4l `README.md` updated: "Integration with execute-work-package" section
- [ ] l4l `docs/CLAUDE_CODE_SETUP.md`: step-by-step CC MCP configuration
- [ ] agent-skills `README.md`: mention l4l under execution backends
- [ ] Known issues / troubleshooting documented

## Acceptance Criteria

- [ ] A real work package (from realworld testbed) executes successfully via CC → l4l MCP
- [ ] Blueprint output matches `tpl-execution-blueprint.md` format
- [ ] Digest output matches `tpl-execution-digest.md` format
- [ ] A new user can follow the docs to set up CC + l4l in <15 minutes
- [ ] No regressions in l4l tests or agent-skills tests

## Dependencies on Other Phases

| Phase | Relationship | Notes |
|-------|-------------|-------|
| Phase 3 | blocked-by | Skill must have Transport section before E2E testing |
| Phase 1-2 | blocked-by | l4l must be stable and format-aligned |

## Notes

- The CC MCP configuration goes in `.claude/settings.json` under `mcpServers`. l4l exposes MCP at `http://localhost:8000/mcp` — this needs to be configured as an SSE or streamable-http transport.
- The E2E test should use a small, well-defined work package (e.g., "add input validation to the orders API" in chimera_project) to keep execution time reasonable.
- Document model selection: recommend a cheap model (Sonnet/Haiku/Devstral) for the Sub-Agent to demonstrate model decoupling.
