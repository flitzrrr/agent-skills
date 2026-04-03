---
type: planning
entity: phase
plan: "l4l-platform-adaptive-execution"
phase: 3
status: completed
created: "2026-04-03"
updated: "2026-04-04"
---

# Phase 3: Skill Transport Adaptation

> Part of [l4l-platform-adaptive-execution](../plan.md)

## Objective

Update the `execute-work-package` SKILL.md to document three transport options (MCP via l4l, Stateful, Fresh Agent) so that any platform can use the skill with its best available mechanism.

## Scope

### Includes

- Replace "Agent Lifecycle" section in SKILL.md with "Transport" section containing 3 options
- Option A (MCP via l4l): `precheck_new` → `approve_blueprint` → `execute` → digest from response
- Option B (Stateful Subagent): Original OpenCode design with `resumeSessionId`
- Option C (Fresh Agent): CC/Cursor/Copilot pattern with separate Agent spawns
- Update `tpl-implementer-preflight-prompt.md` with MCP-aware annotations
- Update `tpl-implementer-execute-prompt.md` with MCP-aware annotations
- Add compatibility metadata: `claude-code`, `cursor`, `copilot`, `codex`, `windsurf`

### Excludes (deferred to later phases)

- E2E testing and documentation (Phase 4)
- Changes to other skills that reference execute-work-package
- New template files (existing templates get annotations, not replaced)

## Prerequisites

- [ ] Phase 2 completed (l4l MCP tools aligned with skill formats)
- [ ] Upstream repo (DasDigitaleMomentum/opencode-processing-skills) access for PR
- [ ] Understand current SKILL.md structure (Protocol section, Output Contracts, Rules)

## Deliverables

- [ ] Updated `SKILL.md` with Transport section (3 options)
- [ ] Updated compatibility metadata in SKILL.md frontmatter
- [ ] Updated `tpl-implementer-preflight-prompt.md` with MCP annotation block
- [ ] Updated `tpl-implementer-execute-prompt.md` with MCP annotation block
- [ ] PR to DasDigitaleMomentum/opencode-processing-skills

## Acceptance Criteria

- [ ] SKILL.md reads coherently with any of the 3 transport options
- [ ] OpenCode users see no change in their workflow (Option B is the original design)
- [ ] CC users can follow Option A (MCP) or Option C (Fresh Agent) without ambiguity
- [ ] Skill templates work for all 3 transports (MCP annotations are additive, not breaking)
- [ ] tisDDM approves the PR (this is his repo)

## Dependencies on Other Phases

| Phase | Relationship | Notes |
|-------|-------------|-------|
| Phase 2 | blocked-by | MCP tool names and format must be finalized first |
| Phase 4 | blocks | E2E validation requires the skill to be updated |

## Notes

- This is the most politically sensitive phase — it modifies tisDDM's skill. The previous PR (#3) was rejected because it changed the stateful design to fresh-only. This approach is additive: the original stateful design becomes Option B, fresh becomes Option C, and MCP becomes the recommended Option A.
- The Transport section should be near the top of the Protocol section, before Step 0.
- Template annotations should use conditional blocks: `<!-- IF MCP: ... -->` / `<!-- IF FRESH: ... -->` to keep templates usable for all transports.
