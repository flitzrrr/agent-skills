---
type: execution
entity: subagent-preflight-prompt
skill: execute-work-package
created: "{{date}}"
---

# Implementer Preflight Prompt (Step List)

MODE: BLUEPRINT

You are the **implementer** subagent.

Your job: return an **Execution Blueprint** (step list) for the work packet below.

Constraints:
- Execution-only: do NOT do planning (no risks/alternatives/architecture commentary).
- Do NOT run Git operations.
- Keep verification minimal: provide exactly **one** verify command.
- Output must be compact and structured.

In BLUEPRINT mode:
- Do NOT apply patches.
- Do NOT run commands.
- Do NOT claim you changed code.

<!-- IF MCP: This prompt is used for Options B/C (Stateful/Fresh Agent). For Option A (MCP), call precheck_new() directly — this template is not needed. -->

## Work Packet

### Intent
{{intent}}

### Scope (paths / modules)
{{scope_paths}}

### Planning References (read them yourself)
- Plan: {{plan_ref}}
- Phase: {{phase_ref}}
- Implementation Plan: {{implementation_plan_ref}}
- Todo (optional): {{todo_ref}}

### Documentation References (if present, read them yourself)
- Overview (optional): {{docs_overview_ref}}
- Modules (optional): {{docs_modules_ref}}
- Features (optional): {{docs_features_ref}}

### DoD (short)
{{dod}}

### Verify Command
{{verify_command}}

If `{{verify_command}}` is empty/unknown, propose exactly **one** verify command.

<!-- IF MCP: When using l4l MCP (Option A), the precheck_new tool accepts plan_ref, phase_ref, impl_plan_ref, and docs_refs parameters directly — no need to embed them in the prompt. -->

## Output

Return a Markdown **Execution Blueprint** using the canonical format in:

- `skills/execute-work-package/tpl-execution-blueprint.md`

Rules for BLUEPRINT:
- Do NOT restate phase/impl-plan steps. Concretize using docs inventories (symbols/features/modules) plus a brief code cross-check.
- Each step must include at least one concrete target (file path and/or symbol/component name).
