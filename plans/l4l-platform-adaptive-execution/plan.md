---
type: planning
entity: plan
plan: "l4l-platform-adaptive-execution"
status: completed
created: "2026-04-03"
updated: "2026-04-04"
---

# Plan: l4l Platform-Adaptive Execution

## Objective

Stabilize l4l as a production-ready MCP execution server and integrate it with the `execute-work-package` skill as the recommended transport — while keeping stateful (OpenCode) and fresh-agent (CC/Cursor/Copilot) transports as documented alternatives.

## Motivation

The `execute-work-package` skill currently hard-couples its protocol (Blueprint → Gate → Execute → Digest) to a single transport mechanism. This breaks across platforms:

- **OpenCode**: Uses stateful `resumeSessionId` — works with original design
- **Claude Code**: Uses ephemeral `Agent` tool — SendMessage to idle agents fails silently
- **Cursor/Copilot/Codex/Windsurf**: Fresh spawns only — no resume capability

l4l already implements the same protocol as an MCP server (precheck → execute → report) but needs stabilization before it can be the recommended default. Once stable, any IDE with MCP support gets the best execution experience — including model decoupling (cheap Sub-LLMs), state persistence, scope enforcement, and iterative blueprint refinement.

## Requirements

### Functional

- [ ] l4l handle state persists across server restarts (currently in-memory only)
- [ ] l4l precheck → execute → report flow works end-to-end with test coverage
- [ ] l4l MCP tools integrate cleanly with the skill's Blueprint/Gate/Execute/Digest protocol
- [ ] `execute-work-package` SKILL.md documents 3 transport options (MCP, Stateful, Fresh)
- [ ] Skill templates (`tpl-implementer-*-prompt.md`) have MCP-aware variants or annotations
- [ ] l4l accepts skill-format Execution Blueprints and returns skill-format Digests

### Non-Functional

- [ ] l4l starts in <5s with `uv pip install -e . && python -m l4l.sub_agent.server`
- [ ] No breaking changes to l4l's existing REST API
- [ ] No breaking changes to the existing skill protocol (OpenCode users unaffected)
- [ ] Test coverage for critical paths (precheck, execute, handle persistence, MCP tools)

## Scope

### In Scope

- l4l handle persistence (disk-backed state)
- l4l test coverage for core flows
- l4l MCP tool alignment with skill templates (blueprint/digest format parity)
- l4l explicit gate step in MCP flow
- `execute-work-package` skill: transport-adaptive lifecycle section
- `execute-work-package` skill: MCP usage examples and prompt annotations
- Documentation for setup and usage across platforms

### Out of Scope

- l4l Lead Agent implementation (only Sub-Agent server)
- l4l streaming responses
- l4l "all" execute mode (stepwise + restricted are sufficient)
- New skill creation (`execute-work-package-cc` variant) — one skill, multiple transports
- Changes to other opencode-processing-skills (create-plan, resume-plan, etc.)
- CI/CD pipeline for l4l
- Claude Code Agent Teams integration (experimental, not stable)

## Definition of Done

- [ ] `python -m pytest tests/` passes with >80% coverage on core service/agent modules
- [ ] l4l server survives restart with handles intact (precheck → restart → execute works)
- [ ] MCP flow produces output matching `tpl-execution-blueprint.md` and `tpl-execution-digest.md` formats
- [ ] `execute-work-package` SKILL.md has Transport section with MCP/Stateful/Fresh options
- [ ] End-to-end demo: Claude Code → l4l MCP → precheck → gate → execute → digest
- [ ] README in l4l documents the skill-integration workflow

## Testing Strategy

- [ ] Unit tests for handle persistence (write, read, recovery after crash)
- [ ] Unit tests for MCP tools (precheck_new, precheck_iterate, execute, handle_report)
- [ ] Integration test: full precheck → execute → report cycle against realworld testbed
- [ ] Manual E2E: Claude Code invokes l4l via MCP, runs a real work package

## Phases

| Phase | Title | Scope | Status |
|-------|-------|-------|--------|
| 1 | l4l Stabilization | Handle persistence + test coverage | completed |
| 2 | Skill-Format Parity | Align l4l output with skill templates, add gate step | completed |
| 3 | Skill Transport Adaptation | Update execute-work-package SKILL.md with multi-transport | completed |
| 4 | E2E Integration & Docs | Wire CC → l4l MCP, document setup, manual validation | completed |

## Risks & Open Questions

| Risk/Question | Impact | Mitigation/Answer |
|---------------|--------|-------------------|
| tisDDM may have different vision for l4l integration | High | Align before Phase 2 starts; Phase 1 is purely stabilization (non-controversial) |
| l4l uses Agno 2.0 framework — unclear if CC MCP client handles Agno's tool format | Medium | Test in Phase 4; l4l MCP adapter already normalizes to standard MCP |
| Handle persistence needs atomic writes to avoid corruption | Medium | Use write-to-temp + rename pattern; test crash recovery |
| Skill template formats may drift from l4l's internal EB/Digest schemas | Low | Phase 2 establishes format parity with explicit mapping |
| OpenCode users should not be affected by skill changes | High | Transport section is additive; original stateful flow preserved as Option B |

## Changelog

### 2026-04-04

- Plan completed — all 4 phases done
- Phase 3 deviation: changes kept local in agent-skills instead of PR to DDM upstream; execute-work-package excluded from sync-skills.sh
- MCP stdio integration test added (5 tests covering full protocol flow)
- Total test suite: 46 tests passing in l4l repo

### 2026-04-03

- Plan created
