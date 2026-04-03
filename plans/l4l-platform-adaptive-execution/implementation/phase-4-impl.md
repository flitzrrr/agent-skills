---
type: planning
entity: implementation-plan
plan: "l4l-platform-adaptive-execution"
phase: 4
status: draft
created: "2026-04-03"
updated: "2026-04-03"
---

# Implementation Plan: Phase 4 - E2E Integration & Docs

> Implements [Phase 4](../phases/phase-4.md) of [l4l-platform-adaptive-execution](../plan.md)

## Approach

Validate the full pipeline end-to-end (Claude Code → l4l MCP → precheck → gate → execute → digest) using a real work package on a testbed project. Then document the setup for CC users (MCP configuration, model selection, troubleshooting). Update both l4l and agent-skills READMEs.

This phase is primarily **validation and documentation** — no production code changes.

## Affected Modules

| Module | Change Type | Description |
|--------|-------------|-------------|
| l4l `README.md` | modify | Add "Integration with execute-work-package" section |
| l4l `docs/CLAUDE_CODE_SETUP.md` | create | Step-by-step CC MCP configuration guide |
| agent-skills `README.md` | modify | Mention l4l as MCP execution backend |
| E2E session transcript | create | Captured CC → l4l MCP run (for validation, not committed) |

## Required Context

| File | Why |
|------|-----|
| l4l `README.md` | Current README to update |
| l4l `l4l.config.yaml` | Configuration reference for docs |
| l4l `src/l4l/sub_agent/mcp/server.py` | MCP tool signatures for docs |
| agent-skills `README.md` | Current README to update |
| Phase 2 `format_skill.py` | Confirms `output_format="skill"` behavior |
| Phase 3 `SKILL.md` | Confirms Transport section Option A text |

## Implementation Steps

### Step 1: Set up CC MCP configuration for l4l

- **What**: Configure Claude Code to use l4l as an MCP server. Create/update `.claude/settings.json` in the test project.
- **Where**: Test project (chimera_project or equivalent testbed)
- **Why**: Required infrastructure for the E2E test.
- **Considerations**:
  - l4l MCP can run via stdio (`python -m l4l.sub_agent.mcp.server`) or SSE/streamable-http (mounted at `/mcp` on the FastAPI server).
  - CC MCP config goes in `.claude/settings.json` under `mcpServers`:
    ```json
    {
      "mcpServers": {
        "l4l": {
          "command": "uv",
          "args": ["run", "--directory", "/path/to/l4l", "python", "-m", "l4l.sub_agent.mcp.server"],
          "env": { "L4L_CONFIG_FILE": "/path/to/l4l/l4l.config.yaml" }
        }
      }
    }
    ```
  - Alternative: SSE transport if l4l server is already running.
  - Document both options in the setup guide.

### Step 2: Run E2E test — CC → l4l MCP → work package execution

- **What**: Execute a small, well-defined work package through the full pipeline using CC with l4l MCP tools.
- **Where**: Testbed project (e.g., "add input validation to orders API" in chimera_project)
- **Why**: Validates the entire integration: MCP tool discovery, precheck_new, approve_blueprint, execute, skill-format output.
- **Considerations**:
  - Use a small scope (1-3 files) to keep execution time reasonable.
  - Configure l4l with a cheap model (Sonnet/Haiku/Devstral) to demonstrate model decoupling.
  - Capture the session as a transcript for reference.
  - Verify:
    1. `precheck_new(output_format="skill")` returns markdown matching blueprint template
    2. `approve_blueprint` succeeds
    3. `execute(output_format="skill")` returns markdown matching digest template
    4. Actual code changes are applied to the testbed
    5. Verify command passes

### Step 3: Write l4l `docs/CLAUDE_CODE_SETUP.md`

- **What**: Step-by-step guide for configuring CC to use l4l MCP.
- **Where**: `/Users/Martin/git/l4l/docs/CLAUDE_CODE_SETUP.md`
- **Why**: A new user should be able to follow this to set up CC + l4l in <15 minutes.
- **Considerations**:
  - Sections:
    1. Prerequisites (Python 3.11+, uv, Claude Code)
    2. Install l4l (`git clone`, `uv pip install -e '.[mcp]'`)
    3. Configure l4l (`l4l.config.yaml` — model selection, data_dir)
    4. Configure CC MCP (`.claude/settings.json` — stdio vs SSE)
    5. Verify setup (`/mcp` command in CC to check tool availability)
    6. First run (example `precheck_new` call)
    7. Troubleshooting (common issues)
  - Include model selection guidance: recommend cheap models (Sonnet/Haiku) for sub-agent, keep Lead on Opus.

### Step 4: Update l4l `README.md`

- **What**: Add "Integration with execute-work-package" section.
- **Where**: `/Users/Martin/git/l4l/README.md`
- **Why**: Users discovering l4l need to understand the skill integration.
- **Considerations**:
  - Brief section (~10-15 lines): what the integration provides, link to `docs/CLAUDE_CODE_SETUP.md`, link to `execute-work-package` skill.
  - Mention the 3 transport options and that l4l enables Option A (MCP).
  - Include the MCP tool list: `precheck_new`, `precheck_iterate`, `approve_blueprint`, `execute`, `handle_report`.

### Step 5: Update agent-skills `README.md`

- **What**: Mention l4l as an MCP execution backend under the execute-work-package skill description.
- **Where**: `/Users/Martin/git/agent-skills/README.md`
- **Why**: Users of agent-skills should know that l4l provides MCP-based execution.
- **Considerations**:
  - Add 2-3 lines under "Planning & Docs" category or as a note after the execute-work-package entry.
  - Link to l4l repo and the setup guide.

### Step 6: Document known issues and troubleshooting

- **What**: Create a troubleshooting section in `CLAUDE_CODE_SETUP.md` (or separate file if large).
- **Where**: Part of Step 3's document
- **Why**: Common issues will surface during E2E testing — capture them.
- **Considerations**:
  - Common issues to document:
    - MCP connection timeout (l4l server not running / wrong transport)
    - Model API key not configured (l4l config references env vars)
    - Scope path errors (absolute vs relative paths)
    - `eb_approved` gate error (forgot to call `approve_blueprint`)
    - Large context / token budget exceeded
  - Format as FAQ: "Problem → Solution" pairs.

## Testing Plan

| Test Type | What to Test | Expected Outcome |
|-----------|-------------|-----------------|
| E2E | CC → l4l MCP → real work package | Blueprint + Digest in skill format, code changes applied |
| Manual | Follow setup guide from scratch | Setup completes in <15 minutes |
| Regression | l4l test suite | No failures from Phases 1-2 |
| Regression | agent-skills test suite | No failures |

**Verify command**: `cd /Users/Martin/git/l4l && uv run pytest tests/ -v && cd /Users/Martin/git/agent-skills && /opt/homebrew/bin/node bin/test-cli.js`

### Test Integrity Constraints

- No existing tests affected — this phase adds documentation and runs manual E2E validation.
- The E2E test is manual (not automated CI) per phase scope.

## Rollback Strategy

- Documentation files can be reverted via `git checkout`.
- No production code changes to roll back.
- CC MCP configuration is project-local (`.claude/settings.json`) — remove entry to disable.

## Open Decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| MCP transport for CC | (A) stdio; (B) SSE; (C) Document both | C — Document both | stdio is simpler for local dev; SSE for persistent server setups |
| Testbed project | chimera_project / phoenix_project | TBD | Depends on which testbed is available and has a small, well-defined task |
| E2E test model | Sonnet / Haiku / Devstral | Sonnet | Good balance of capability and cost for demonstrating model decoupling |

## Reality Check

### Code Anchors Used

| File | Symbol/Area | Why it matters |
|------|-------------|----------------|
| l4l `src/l4l/sub_agent/mcp/server.py:55` | `mcp = FastMCP("l4l-sub-agent")` | Server name for MCP discovery |
| l4l `src/l4l/sub_agent/mcp/server.py:250-256` | `main()` → `mcp.run()` | stdio entrypoint for CC config |
| l4l `l4l.config.yaml` | Server and model config | Referenced in setup guide |
| l4l `src/l4l/sub_agent/config.py:74` | `data_dir: str = ".l4l"` | Default data dir for docs |
| agent-skills `README.md` | Current structure | Where to add l4l mention |

### Mismatches / Notes

- The phase doc mentions "chimera_project or phoenix_project" as testbeds. These may not be available locally — the E2E test step should document how to create a minimal testbed if these aren't present.
- l4l's MCP server (`mcp/server.py`) has a `main()` that calls `mcp.run()` for stdio. For SSE, the FastAPI app mounts MCP at `/mcp`. The docs must distinguish these two modes clearly.
- CC's MCP configuration for stdio requires the full command path. Since the user's environment has PATH issues (e.g., `uv` might not be in default PATH), the docs should recommend absolute paths or PATH exports in the config.
- The `approve_blueprint` MCP tool is new (Phase 2). If Phase 2 isn't complete yet, the E2E test will use `native` format without the gate — document this as a known limitation.
