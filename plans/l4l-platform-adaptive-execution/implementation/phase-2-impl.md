---
type: planning
entity: implementation-plan
plan: "l4l-platform-adaptive-execution"
phase: 2
status: draft
created: "2026-04-03"
updated: "2026-04-03"
---

# Implementation Plan: Phase 2 - Skill-Format Parity

> Implements [Phase 2](../phases/phase-2.md) of [l4l-platform-adaptive-execution](../plan.md)

## Approach

Add a thin output-formatting layer in l4l that converts its internal `ExecutionBlueprint` and `ExecuteResponse` into the markdown formats expected by the `execute-work-package` skill templates. Add an explicit `approve_blueprint` MCP tool that gates execution. Add `output_format` parameter to MCP tools. This is an **additive** layer — l4l's internal schemas and behavior stay unchanged.

## Affected Modules

| Module | Change Type | Description |
|--------|-------------|-------------|
| `src/l4l/sub_agent/service/format_skill.py` | create | EB → skill blueprint markdown, ExecuteResponse → skill digest markdown |
| `src/l4l/sub_agent/mcp/server.py` | modify | Add `approve_blueprint` tool, add `output_format` param to existing tools |
| `src/l4l/sub_agent/api/state.py` | modify | Add `eb_approved` field tracking to handle state |
| `src/l4l/sub_agent/schemas.py` | modify | Add `eb_approved: bool` and optional plan/doc refs to `HandleState` and `SubSTS` |
| `tests/sub_agent/test_format_skill.py` | create | Format conversion tests |
| `tests/sub_agent/test_approve_gate.py` | create | Gate enforcement tests |

## Required Context

| File | Why |
|------|-----|
| `src/l4l/harness/models.py` | `ExecutionBlueprint`, `EBStep`, `Action`, `Observation` — source format |
| `src/l4l/sub_agent/schemas.py` | `HandleState`, `ExecuteResponse`, `PrecheckResponse` — what gets formatted |
| `src/l4l/sub_agent/mcp/server.py` | MCP tool definitions — where `output_format` and `approve_blueprint` go |
| `src/l4l/sub_agent/service/sub_agent_service.py` | Service layer — `execute_handle()` must check approval |
| `vendor/.../tpl-execution-blueprint.md` | Target markdown format for blueprints |
| `vendor/.../tpl-execution-digest.md` | Target markdown format for digests |
| Phase 1 impl plan | `state.py` persistence must be stable before adding fields |

## Implementation Steps

### Step 1: Add plan/doc reference fields to `SubSTS` and `HandleState`

- **What**: Add optional fields `plan_ref`, `phase_ref`, `impl_plan_ref`, `todo_ref`, `docs_overview_ref`, `docs_modules_ref`, `docs_features_ref` to `SubSTS`. Add `eb_approved: bool = False` to `HandleState`.
- **Where**: `src/l4l/sub_agent/schemas.py` — `SubSTS` (line 72-97) and `HandleState` (line 231-264)
- **Why**: The skill blueprint template requires plan/doc references. The gate needs an approval flag.
- **Considerations**: All new fields must be optional with defaults so existing code and tests are unaffected. `eb_approved` resets to `False` on each new EB version (handle in `save_handle` or service layer).

### Step 2: Create `format_skill.py` — EB → skill blueprint markdown

- **What**: Write a function `format_blueprint_as_skill(handle: HandleState, response: PrecheckResponse) -> str` that produces markdown matching `tpl-execution-blueprint.md`.
- **Where**: `src/l4l/sub_agent/service/format_skill.py`
- **Why**: The skill template expects specific headings: `# Execution Blueprint (Step List)`, `## Work Packet`, `## References`, `## Steps`, `## Touched Files`, `## Verify`.
- **Considerations**:
  - Map `EBStep` to numbered steps: `1. [{action}] {target or scope} — {rationale}`
  - Extract touched files from steps with `action` in `(modify, create)` → collect unique `target` values.
  - Extract verify command from steps with `action == verify` → use `selector`.
  - Populate `## References` from the new `SubSTS` plan/doc fields.
  - If fields are None, omit the reference line (don't emit `None`).

### Step 3: Create `format_skill.py` — ExecuteResponse → skill digest markdown

- **What**: Write a function `format_digest_as_skill(handle: HandleState, response: ExecuteResponse) -> str` that produces markdown matching `tpl-execution-digest.md`.
- **Where**: Same file `src/l4l/sub_agent/service/format_skill.py`
- **Why**: The skill digest template expects: `### Outcome`, `### Edits`, `### Verify`, `### Next`.
- **Considerations**:
  - `state` field maps directly: `succeeded` / `failed`.
  - `Edits` → extract from `EditObservation` digests in response observations. Each `EditDigestChanged` has `file`, `added`, `removed`. Format as `- path/to/file — {added} added, {removed} removed`.
  - `Verify` → extract from `TestObservation` or `ProcessObservation` digests. Use `selector`/`cmd`, `exit`, and `first_lines` for excerpt.
  - `Next` → derive from response `warnings` and `state`. If succeeded: "Proceed to next phase". If failed: summarize error.

### Step 4: Add `approve_blueprint` MCP tool

- **What**: New MCP tool that marks the current EB as approved. `execute` must refuse to run on unapproved EBs.
- **Where**: `src/l4l/sub_agent/mcp/server.py` — add between `precheck_iterate` and `execute` tools.
- **Why**: Mirrors the skill's "Primary provides explicit approval token" invariant. This is the GATE step.
- **Considerations**:
  - Parameters: `handle_id: str`, `feedback: str | None = None` (optional approval feedback).
  - Logic: `get_handle(handle_id)` → check `current_eb` exists → set `handle.eb_approved = True` → `save_handle()`.
  - If `feedback` is provided, optionally store it but don't trigger a precheck iteration (that's what `precheck_iterate` is for).
  - Return: `{"handle_id": ..., "eb_version": ..., "approved": True}`.
  - Add guard in `execute` MCP tool: if `handle.eb_approved is False`, raise error "EB must be approved before execution. Call approve_blueprint first."

### Step 5: Add `output_format` parameter to MCP tools

- **What**: Add `output_format: Literal["native", "skill"] = "native"` parameter to `precheck_new`, `precheck_iterate`, and `execute` MCP tools.
- **Where**: `src/l4l/sub_agent/mcp/server.py`
- **Why**: When `output_format="skill"`, return skill-compatible markdown string instead of raw dict.
- **Considerations**:
  - When `output_format="native"` (default): existing behavior unchanged — return `resp.model_dump()`.
  - When `output_format="skill"`: call the format function, return `{"handle_id": ..., "formatted": "<markdown>", "format": "skill"}`.
  - The `handle_report` tool does not need `output_format` (it's a debug tool).

### Step 6: Add plan/doc ref parameters to `precheck_new` MCP tool

- **What**: Accept optional `plan_ref`, `phase_ref`, `impl_plan_ref`, `docs_refs` parameters in the `precheck_new` MCP tool.
- **Where**: `src/l4l/sub_agent/mcp/server.py` — `precheck_new` function signature.
- **Why**: These refs are stored in the STS and used for skill blueprint formatting. They also get passed through to sub-agent prompts as file references for context.
- **Considerations**:
  - These are file paths relative to `project_root`. The sub-agent reads them during precheck if `precheck_mode=explore`.
  - Store in `SubSTS.context` field (append as structured text) or in the new dedicated fields.

### Step 7: Write tests

- **What**: Test format conversion (both directions) and gate enforcement.
- **Where**: `tests/sub_agent/test_format_skill.py`, `tests/sub_agent/test_approve_gate.py`
- **Why**: Verify format output matches template structure and gate prevents unauthorized execution.
- **Considerations**:
  - `test_format_skill.py`:
    - Test blueprint format contains expected headings (`## Steps`, `## Touched Files`, `## Verify`).
    - Test digest format contains expected sections (`### Outcome`, `### Edits`, `### Verify`).
    - Test with empty observations (edge case).
    - Test with missing plan refs (fields should be omitted, not `None`).
  - `test_approve_gate.py`:
    - Test `execute` raises when `eb_approved=False`.
    - Test `approve_blueprint` sets flag.
    - Test flag resets on new EB version (precheck_iterate after approval).

## Testing Plan

| Test Type | What to Test | Expected Outcome |
|-----------|-------------|-----------------|
| Unit | `test_format_skill.py` — EB → blueprint markdown | Markdown matches template headings and structure |
| Unit | `test_format_skill.py` — Response → digest markdown | Markdown matches template sections |
| Unit | `test_approve_gate.py` — gate enforcement | Execute blocked without approval, allowed after |
| Regression | All existing tests + Phase 1 tests | No failures |

**Verify command**: `cd /Users/Martin/git/l4l && uv run pytest tests/ -v`

### Test Integrity Constraints

- `tests/sub_agent/test_sub_agent_service.py`: May need minor update if `execute_handle` now checks `eb_approved`. The existing test creates handles with `eb_approved` defaulting to `False` — either (a) the test must set `eb_approved=True` before calling execute, or (b) the approval gate is only enforced in the MCP layer, not the service layer. **Recommend (b)**: keep service layer permissive, enforce gate only in MCP adapter.
- All other existing tests: No changes expected.

## Rollback Strategy

- `format_skill.py` is a new file — delete to revert.
- MCP changes are additive (new tool, new optional params) — remove to revert.
- Schema field additions are optional with defaults — safe to revert.

## Open Decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| Gate enforcement layer | (A) Service layer; (B) MCP adapter only | B — MCP only | Keeps service layer simple; REST API callers can manage their own gating |
| `output_format` return type | (A) String (markdown); (B) Dict with `formatted` key | B — Dict | Consistent with native format (always dict); includes handle_id for correlation |
| `eb_approved` reset | (A) Reset on precheck_iterate; (B) Reset on any EB version change | A — precheck_iterate | Same trigger: iterate = new EB version = needs re-approval |

## Reality Check

### Code Anchors Used

| File | Symbol/Area | Why it matters |
|------|-------------|----------------|
| `src/l4l/harness/models.py:136-167` | `EBStep` fields: `action`, `scope`, `target`, `selector`, `rationale`, `note` | These map to blueprint step lines |
| `src/l4l/harness/models.py:196-206` | `ExecutionBlueprint.steps` | Source of step list for blueprint format |
| `src/l4l/harness/models.py:238-260` | `EditDigest`, `TestDigest`, `ProcessDigest` | Source of edit/verify data for digest format |
| `src/l4l/sub_agent/schemas.py:190-215` | `ExecuteResponse` fields | `state`, `observations`, `steps_completed` map to digest sections |
| `src/l4l/sub_agent/mcp/server.py:74-136` | `precheck_new` MCP tool | Where `output_format` and plan refs get added |
| `src/l4l/sub_agent/mcp/server.py:180-217` | `execute` MCP tool | Where gate check and `output_format` get added |
| `vendor/.../tpl-execution-blueprint.md` | Skill template | Target format: `## Steps`, `## Touched Files`, `## Verify` headings |
| `vendor/.../tpl-execution-digest.md` | Skill template | Target format: `### Outcome`, `### Edits`, `### Verify`, `### Next` |

### Mismatches / Notes

- The skill blueprint template has a `## References` section with `plan`, `phase`, `implementation_plan`, `todo`, `docs` sub-fields. l4l's `SubSTS` currently has no plan/doc reference fields. Step 1 addresses this.
- The skill digest `### Edits` section expects `files_changed` with one-line summaries. l4l's `EditDigest` has `file`, `added`, `removed` counts but no semantic summary. The format function will generate summaries from counts (e.g., "3 added, 1 removed").
- The `approve_blueprint` tool is entirely new — no existing l4l concept maps to it. The closest is that `execute` currently runs on any EB without gating. The gate is additive.
- `output_format` affects only the MCP return value, not internal storage. Artifacts written to disk (via `logging.py`) always use the native format.
