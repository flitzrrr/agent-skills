---
type: planning
entity: phase
plan: "l4l-platform-adaptive-execution"
phase: 2
status: completed
created: "2026-04-03"
updated: "2026-04-04"
---

# Phase 2: Skill-Format Parity

> Part of [l4l-platform-adaptive-execution](../plan.md)

## Objective

Align l4l's MCP output formats with the `execute-work-package` skill templates so that a Lead Agent can use l4l's MCP tools and get back Execution Blueprints and Digests in the exact format the skill expects.

## Scope

### Includes

- Map l4l's `ExecutionBlueprint` schema to `tpl-execution-blueprint.md` format
- Map l4l's execute response to `tpl-execution-digest.md` format
- Add explicit gate step in MCP flow: `precheck_new` → `approve_blueprint` (new tool) → `execute`
- Ensure l4l's precheck accepts `plans/` and `docs/` references as STS context
- Add `output_format` parameter to MCP tools (default: `skill` for skill-compatible output, `native` for l4l's internal format)

### Excludes (deferred to later phases)

- Modifying the SKILL.md itself (Phase 3)
- E2E testing with Claude Code (Phase 4)
- Changing l4l's internal EB/Observation schemas (only the MCP output layer adapts)

## Prerequisites

- [ ] Phase 1 completed (stable handle persistence, tests passing)
- [ ] Understand skill template formats: `tpl-execution-blueprint.md`, `tpl-execution-digest.md`
- [ ] Understand l4l's `ExecutionBlueprint` and `Observation` Pydantic schemas

## Deliverables

- [ ] MCP tool `approve_blueprint(handle_id, approval_token, feedback?)` — explicit gate
- [ ] Output formatter: `l4l EB → skill blueprint markdown` (matching template headings)
- [ ] Output formatter: `l4l execute response → skill digest markdown` (matching template headings)
- [ ] `output_format` parameter on `precheck_new` and `execute` MCP tools
- [ ] STS accepts optional `plan_ref`, `phase_ref`, `impl_plan_ref`, `docs_refs` fields
- [ ] Tests for format conversion (round-trip: skill format → l4l → skill format)

## Acceptance Criteria

- [ ] `precheck_new(output_format="skill")` returns markdown matching `tpl-execution-blueprint.md` structure
- [ ] `execute(output_format="skill")` returns markdown matching `tpl-execution-digest.md` structure
- [ ] `approve_blueprint` prevents execute without explicit approval (returns error if not approved)
- [ ] Existing `output_format="native"` (default) behavior unchanged — no breaking changes
- [ ] `plan_ref`/`phase_ref` in STS are passed to sub-agent prompts as file references

## Dependencies on Other Phases

| Phase | Relationship | Notes |
|-------|-------------|-------|
| Phase 1 | blocked-by | Needs stable handle persistence |
| Phase 3 | blocks | Skill update references the MCP tools and format |

## Notes

- The format conversion is a thin layer on top of l4l's existing output — not a rewrite. l4l's internal `ExecutionBlueprint` has `steps: list[Action]` where each Action has `type`, `target`, `rationale`, `details`. The skill blueprint wants a numbered step list with file paths and concretized targets.
- The gate step (`approve_blueprint`) mirrors the skill's "Primary provides explicit approval token" invariant. It mutates the handle state to mark the EB as approved, and `execute` refuses to run on unapproved EBs.
- tisDDM should review the format mapping before implementation to ensure it doesn't conflict with l4l's design intent.
