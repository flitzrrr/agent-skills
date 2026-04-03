---
type: planning
entity: implementation-plan
plan: "l4l-platform-adaptive-execution"
phase: 3
status: draft
created: "2026-04-03"
updated: "2026-04-03"
---

# Implementation Plan: Phase 3 - Skill Transport Adaptation

> Implements [Phase 3](../phases/phase-3.md) of [l4l-platform-adaptive-execution](../plan.md)

## Approach

Replace the "Agent Lifecycle" section in SKILL.md with a "Transport" section documenting three options: MCP via l4l (Option A), Stateful Subagent (Option B, original OpenCode design), and Fresh Agent (Option C, CC/Cursor/Copilot). This is **additive** — Option B preserves the original stateful design exactly, Option C is the current "Agent Lifecycle" text, and Option A is the new MCP path. Add conditional annotations to templates for MCP-specific behavior. Update compatibility metadata.

This phase targets the upstream repo `DasDigitaleMomentum/opencode-processing-skills` — changes are authored as a PR.

## Affected Modules

| Module | Change Type | Description |
|--------|-------------|-------------|
| `skills/execute-work-package/SKILL.md` | modify | Replace "Agent Lifecycle" with "Transport" section (3 options) |
| `skills/execute-work-package/tpl-implementer-preflight-prompt.md` | modify | Add MCP annotation block |
| `skills/execute-work-package/tpl-implementer-execute-prompt.md` | modify | Add MCP annotation block |
| `skills/execute-work-package/SKILL.md` frontmatter | modify | Add compatibility metadata for CC, Cursor, Copilot, Codex, Windsurf |

## Required Context

| File | Why |
|------|-----|
| `vendor/.../skills/execute-work-package/SKILL.md` | Current skill — the file to modify |
| `vendor/.../skills/execute-work-package/tpl-implementer-preflight-prompt.md` | Template to annotate |
| `vendor/.../skills/execute-work-package/tpl-implementer-execute-prompt.md` | Template to annotate |
| `vendor/.../skills/execute-work-package/tpl-execution-blueprint.md` | Blueprint format (referenced, not modified) |
| `vendor/.../skills/execute-work-package/tpl-execution-digest.md` | Digest format (referenced, not modified) |
| Phase 2 impl plan | MCP tool names (`precheck_new`, `approve_blueprint`, `execute`) must be finalized |

## Implementation Steps

### Step 1: Update SKILL.md frontmatter — compatibility metadata

- **What**: Expand the `compatibility` section to include all supported platforms with their transport option.
- **Where**: `SKILL.md` lines 5-7 (frontmatter)
- **Why**: Agents on different platforms need to know which transport option applies to them.
- **Considerations**:
  - Current: `compatibility: { opencode: ">=0.1" }`
  - New:
    ```yaml
    compatibility:
      opencode: ">=0.1"
      claude-code: ">=1.0"
      cursor: ">=0.40"
      copilot: ">=1.0"
      codex: ">=0.1"
      windsurf: ">=1.0"
    ```
  - Version numbers are approximate — use the earliest version that supports Agent/subagent spawning.

### Step 2: Replace "Agent Lifecycle" with "Transport" section

- **What**: Remove the current "Agent Lifecycle" subsection (SKILL.md lines 73-80) and replace it with a "Transport" section containing three options. Place it within the "Execution Model" section, after "Routing Matrix".
- **Where**: `SKILL.md` — between "Why `docs/` and `plans/` matter here" and "## Protocol"
- **Why**: The current section only describes the fresh agent pattern. The new section must present all three transport options so each platform can use its best mechanism.
- **Considerations**:
  - **Option A (MCP via l4l)** — Recommended when l4l is available:
    - BLUEPRINT: `precheck_new(output_format="skill")` → returns skill-format blueprint
    - GATE: `approve_blueprint(handle_id)` → explicit gate
    - EXECUTE: `execute(handle_id, output_format="skill")` → returns skill-format digest
    - Iteration: `precheck_iterate(handle_id, feedback)` before re-approval
    - Advantage: Handle persistence, model decoupling, artifact logging
  - **Option B (Stateful Subagent)** — OpenCode / platforms with `resumeSessionId`:
    - BLUEPRINT: spawn subagent, get step list, keep session alive
    - GATE: primary reviews, approves with token
    - EXECUTE: resume same session via `resumeSessionId` or equivalent
    - Advantage: Full context preserved across gate
  - **Option C (Fresh Agent)** — CC Agent tool / Cursor / Copilot / Codex / Windsurf:
    - BLUEPRINT: spawn Agent with preflight prompt, get step list, agent terminates
    - GATE: primary reviews, approves
    - EXECUTE: spawn **new** Agent with execute prompt + full approved step list
    - The EXECUTE agent has no memory of the BLUEPRINT agent — prompt must be self-contained
    - This is the current "Agent Lifecycle" text, preserved verbatim
  - Include a decision table: platform → recommended transport option.
  - Keep the section concise — each option should be ~5-8 lines.

### Step 3: Update Protocol section references

- **What**: In the Protocol section (Steps 1 and 2), add transport-conditional notes where the flow differs.
- **Where**: `SKILL.md` Protocol section (lines 86-162)
- **Why**: Step 1 (BLUEPRINT) and Step 2 (EXECUTE) behave differently depending on transport.
- **Considerations**:
  - Step 1 (BLUEPRINT): Add note: "If using MCP transport (Option A): call `precheck_new` instead of spawning a subagent."
  - Step 1 (GATE): Add note: "If using MCP transport: call `approve_blueprint(handle_id)`. If using Option B/C: primary provides approval token in-context."
  - Step 2 (EXECUTE): Add note: "If using MCP transport: call `execute(handle_id)`. If using Option B: resume session. If using Option C: spawn new Agent."
  - Keep notes brief — use `> **MCP (Option A):**` blockquote style.

### Step 4: Add MCP annotations to `tpl-implementer-preflight-prompt.md`

- **What**: Add a conditional MCP annotation block that tells the agent how to use MCP tools instead of direct execution.
- **Where**: `tpl-implementer-preflight-prompt.md` — after the `## Work Packet` section, before `## Output`
- **Why**: When the orchestrator uses MCP, the preflight prompt is replaced by a `precheck_new` call. The annotation documents this equivalence.
- **Considerations**:
  - Use HTML comment blocks for annotations: `<!-- IF MCP: This prompt is replaced by precheck_new(intent=..., scope_paths=..., output_format="skill") -->`
  - The annotation is informational — it doesn't change the template for non-MCP users.
  - Also annotate the plan/doc reference slots with the corresponding MCP parameter names.

### Step 5: Add MCP annotations to `tpl-implementer-execute-prompt.md`

- **What**: Add a conditional MCP annotation block for the execute prompt.
- **Where**: `tpl-implementer-execute-prompt.md` — after the mode indicator, before `## Approved Step List`
- **Why**: Same rationale as Step 4 — document the MCP equivalence.
- **Considerations**:
  - `<!-- IF MCP: This prompt is replaced by execute(handle_id, output_format="skill"). The EB must be approved via approve_blueprint first. -->`
  - Annotate the verify command slot: `<!-- IF MCP: Verify is handled by l4l's execute step (action=verify). -->`

### Step 6: Review and PR preparation

- **What**: Self-review the changes for coherence across all three transport options. Ensure Option B (stateful) reads exactly as the original design. Prepare PR to `DasDigitaleMomentum/opencode-processing-skills`.
- **Where**: All modified files
- **Why**: This is politically sensitive — tisDDM rejected the previous PR (#3) that replaced statefulness. This approach must be clearly additive.
- **Considerations**:
  - PR title should emphasize "additive": e.g., "Add multi-transport support (MCP + Fresh Agent) alongside stateful design"
  - PR description should explain: Option B IS the original design, untouched. Options A and C are additive.
  - Tag tisDDM for review.

## Testing Plan

| Test Type | What to Test | Expected Outcome |
|-----------|-------------|-----------------|
| Manual | Read SKILL.md with Option A mindset | Clear MCP workflow, no ambiguity |
| Manual | Read SKILL.md with Option B mindset | Identical to original OpenCode workflow |
| Manual | Read SKILL.md with Option C mindset | Clear fresh-agent workflow (current behavior) |
| Manual | Templates still parse for non-MCP users | Annotations are HTML comments, invisible in rendered markdown |

**Verify command**: `cd /Users/Martin/git/agent-skills && grep -c "Option A\|Option B\|Option C" vendor/opencode-processing-skills/skills/execute-work-package/SKILL.md`

(Expected: at least 3 occurrences, one per option definition plus references in Protocol.)

### Test Integrity Constraints

- No existing tests affected — this phase modifies markdown skill documentation only.
- agent-skills test suite (`bin/test-cli.js`) should still pass as it tests CLI functionality, not skill content.

## Rollback Strategy

- All changes are in markdown files — `git checkout` to revert.
- PR can be closed without merge if tisDDM objects.

## Open Decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| Transport section placement | (A) Before Protocol; (B) Within Execution Model | B — Within Execution Model | Replaces "Agent Lifecycle" which is already in Execution Model |
| Annotation style | (A) HTML comments `<!-- IF MCP: ... -->`; (B) Dedicated subsections | A — HTML comments | Non-intrusive for non-MCP users; invisible in rendered markdown |
| Option ordering | (A) MCP first; (B) Stateful first; (C) Fresh first | A — MCP first | MCP is the recommended option; but Option B is clearly labeled as the original design |

## Reality Check

### Code Anchors Used

| File | Symbol/Area | Why it matters |
|------|-------------|----------------|
| `SKILL.md:73-80` | "Agent Lifecycle" section | The section to replace with "Transport" |
| `SKILL.md:5-7` | `compatibility:` frontmatter | Where to add platform metadata |
| `SKILL.md:106-126` | Protocol Steps 1-2 | Where transport-conditional notes go |
| `tpl-implementer-preflight-prompt.md:1-50` | Full template | Where MCP annotation goes |
| `tpl-implementer-execute-prompt.md:1-40` | Full template | Where MCP annotation goes |
| Phase 2 `mcp/server.py` | MCP tool names | `precheck_new`, `approve_blueprint`, `execute` — referenced in Option A |

### Mismatches / Notes

- The phase doc mentions "Replace Agent Lifecycle section" but the current section is only 8 lines (73-80). The replacement "Transport" section will be significantly longer (~40-50 lines for 3 options + decision table). This is acceptable — the section needs to be comprehensive.
- tisDDM's original design uses `resumeSessionId` which is OpenCode-specific. Option B should use this term explicitly to show it's preserved. The previous PR #3 was rejected because it removed this — we must not.
- The template annotations use HTML comments which are standard markdown but may not render in all viewers. This is acceptable as they're informational, not functional.
- The PR targets `DasDigitaleMomentum/opencode-processing-skills`, not `flitzrrr/agent-skills`. The agent-skills repo vendors this skill via submodule — after the upstream PR merges, a submodule update brings the changes in.
