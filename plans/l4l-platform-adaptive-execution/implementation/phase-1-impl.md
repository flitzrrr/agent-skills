---
type: planning
entity: implementation-plan
plan: "l4l-platform-adaptive-execution"
phase: 1
status: draft
created: "2026-04-03"
updated: "2026-04-03"
---

# Implementation Plan: Phase 1 - l4l Stabilization

> Implements [Phase 1](../phases/phase-1.md) of [l4l-platform-adaptive-execution](../plan.md)

## Approach

Replace the in-memory `_handles` dict in `state.py` with disk-backed persistence using Pydantic's `model_dump_json()` / `model_validate_json()`. Handle state files live alongside existing artifacts under `{data_dir}/handles/{handle_id}/`. On server startup, scan existing handle directories and load their state files into the in-memory dict (warm cache). All writes use atomic temp-file + rename to prevent corruption.

The existing artifact persistence (EB versions, logs, observations via `logging.py`) is untouched — only the `HandleState` object gets disk persistence.

## Affected Modules

| Module | Change Type | Description |
|--------|-------------|-------------|
| `src/l4l/sub_agent/api/state.py` | modify | Rewrite with disk-backed persistence + atomic writes |
| `src/l4l/sub_agent/api/app.py` | modify | Call `load_all_handles()` on startup |
| `tests/sub_agent/test_state_persistence.py` | create | Persistence-specific tests |
| `tests/sub_agent/test_mcp_tools.py` | create | MCP tool integration tests |
| `tests/sub_agent/test_e2e_flow.py` | create | End-to-end precheck→execute flow test |

## Required Context

| File | Why |
|------|-----|
| `src/l4l/sub_agent/api/state.py` | The 42-line file to rewrite |
| `src/l4l/sub_agent/schemas.py` | `HandleState` Pydantic model (line 231-264) — what gets serialized |
| `src/l4l/sub_agent/config.py` | `get_data_dir()` — determines where handle dirs live |
| `src/l4l/sub_agent/api/logging.py` | `_ensure_handle_dir()` — already creates `{data_dir}/handles/{handle_id}/` |
| `src/l4l/sub_agent/service/sub_agent_service.py` | Calls `save_handle()`, `get_handle()`, `generate_handle_id()` |
| `tests/sub_agent/test_sub_agent_service.py` | Existing test patterns: monkeypatch, `_clean_handle_storage` fixture |
| `tests/conftest.py` | `tmp_project_dir` fixture, config env setup |

## Implementation Steps

### Step 1: Rewrite `state.py` with disk-backed persistence

- **What**: Replace the in-memory-only `_handles` dict with a hybrid approach: keep the dict as a warm cache, but every `save_handle()` also writes `handle_state.json` to disk, and `get_handle()` falls back to disk if not in cache. Add `load_all_handles()` to scan existing handle directories on startup. Add `delete_handle()` that removes both cache entry and disk file.
- **Where**: `src/l4l/sub_agent/api/state.py`
- **Why**: Handles must survive server restarts — this is the critical gap blocking MCP integration.
- **Considerations**:
  - Use `_ensure_handle_dir()` from `logging.py` (or import `get_data_dir()` from `config.py`) for the handle directory path.
  - Atomic writes: write to `handle_state.json.tmp` then `os.replace()` to `handle_state.json`. `os.replace()` is atomic on POSIX.
  - `load_all_handles()` must tolerate corrupt/missing state files gracefully (log warning, skip).
  - Keep the `_handles` dict as module-level state (same pattern as now) for test isolation via monkeypatch.
  - The `HandleState` Pydantic model already supports `model_dump_json()` and `model_validate_json()` — no schema changes needed.
  - File name: `handle_state.json` (distinct from existing artifacts like `eb.latest.json`).

### Step 2: Wire startup loading in `app.py`

- **What**: Call `load_all_handles()` during FastAPI app startup so that existing handles are available immediately after server restart.
- **Where**: `src/l4l/sub_agent/api/app.py` — look for the existing `lifespan` or `on_startup` hook.
- **Why**: Without startup loading, restarted servers would 404 on all existing handles.
- **Considerations**:
  - If `app.py` uses `@app.on_event("startup")` or a `lifespan` context manager, add the call there.
  - Log the number of handles loaded at INFO level.
  - If no startup hook exists, add a `lifespan` async context manager (FastAPI pattern).

### Step 3: Write `tests/sub_agent/test_state_persistence.py`

- **What**: Test the new persistence behavior in isolation.
- **Where**: `tests/sub_agent/test_state_persistence.py`
- **Why**: Verify atomic writes, load-on-startup, corrupt-file tolerance, and cache coherence.
- **Considerations**:
  - Tests must use `tmp_path` and monkeypatch `get_data_dir()` to point at a temp directory.
  - Test cases:
    1. `save_handle` writes `handle_state.json` to disk
    2. `get_handle` loads from disk when not in cache
    3. `load_all_handles` populates cache from disk
    4. `load_all_handles` skips corrupt JSON files (log warning, don't crash)
    5. `delete_handle` removes both cache and disk file
    6. Atomic write: if process dies mid-write, no partial `handle_state.json` (test that `.tmp` is cleaned up)

### Step 4: Write `tests/sub_agent/test_mcp_tools.py`

- **What**: Test MCP tool functions at the service boundary (not through HTTP).
- **Where**: `tests/sub_agent/test_mcp_tools.py`
- **Why**: Verify MCP adapter delegates correctly to service layer.
- **Considerations**:
  - Monkeypatch `_precheck_new`, `_precheck_iterate`, `_execute_handle` in `mcp/server.py` to return canned responses.
  - Test that MCP tools normalize enum values (string → PrecheckMode/ExecuteMode).
  - Test that `precheck_new` returns a dict with `handle_id`, `eb`, `eb_version`.
  - Test `handle_report` returns artifact paths.

### Step 5: Write `tests/sub_agent/test_e2e_flow.py`

- **What**: Test the full flow: `precheck_new` → `precheck_iterate` → `execute` using the service layer with stubbed agent calls.
- **Where**: `tests/sub_agent/test_e2e_flow.py`
- **Why**: Verify the complete lifecycle works end-to-end at the service layer.
- **Considerations**:
  - Stub `run_precheck_new`, `run_precheck_iterate`, `run_execute` (the agent runners) to return canned EBs/observations.
  - Verify: handle persists across calls, EB versions increment, observations accumulate, state transitions are correct.
  - Use `tmp_path` for both project root and data dir.

### Step 6: Verify all existing tests pass

- **What**: Run the full test suite to ensure no regressions.
- **Where**: Project root
- **Why**: The `_clean_handle_storage` fixture in existing tests monkeypatches `state._handles = {}`. The new code must still work with this pattern (clear cache = clear in-memory dict; disk reads are bypassed because `_handles` is patched).
- **Considerations**:
  - The existing `test_sub_agent_service.py` monkeypatches `state._handles` directly. Since we keep `_handles` as the module-level dict, this still works.
  - The key risk: if `get_handle()` now falls back to disk, monkeypatched tests might accidentally read stale state from disk. Mitigation: also monkeypatch `get_data_dir()` in the clean fixture, or ensure `get_handle()` only reads from `_handles` dict (not disk) when the dict is explicitly set.

## Testing Plan

| Test Type | What to Test | Expected Outcome |
|-----------|-------------|-----------------|
| Unit | `test_state_persistence.py` — save/load/delete/corrupt tolerance | All pass, atomic writes verified |
| Unit | `test_mcp_tools.py` — MCP adapter delegation | All pass, enum normalization works |
| Integration | `test_e2e_flow.py` — full precheck→execute lifecycle | Handle state persists, EB versions increment |
| Regression | All existing tests | No failures |

**Verify command**: `cd /Users/Martin/git/l4l && uv run pytest tests/ -v`

### Test Integrity Constraints

- `tests/sub_agent/test_sub_agent_service.py`: Must remain untouched. The `_clean_handle_storage` fixture monkeypatches `state._handles = {}` — this pattern must continue to work with the new persistence code.
- `tests/conftest.py`: Must remain untouched. Config env setup is compatible.
- `tests/sub_agent/test_handle_report_service.py`: Must remain untouched. Tests handle artifact discovery, not state persistence.

## Rollback Strategy

- `state.py` is 42 lines — easy to revert via `git checkout`.
- New test files can simply be deleted.
- `app.py` change is a single `load_all_handles()` call — remove it to revert.

## Open Decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| Cache vs. disk-only reads | (A) Always read from cache, disk is write-through; (B) Always read from disk | A — Write-through cache | Performance: avoid disk I/O on every `get_handle()`. Cache is authoritative after startup load. |
| State file name | `handle_state.json` vs `state.json` | `handle_state.json` | Avoids collision with potential future files; self-documenting |
| Corrupt file handling | (A) Skip + warn; (B) Raise + abort startup | A — Skip + warn | Resilience: one corrupt handle shouldn't block all others |

## Reality Check

### Code Anchors Used

| File | Symbol/Area | Why it matters |
|------|-------------|----------------|
| `src/l4l/sub_agent/api/state.py:14` | `_handles: dict[str, HandleState] = {}` | The in-memory dict to augment with disk persistence |
| `src/l4l/sub_agent/api/state.py:31-34` | `save_handle()` | Current save: only updates dict + timestamp. Must add disk write. |
| `src/l4l/sub_agent/api/state.py:24-28` | `get_handle()` | Current get: dict lookup + 404. Must add disk fallback. |
| `src/l4l/sub_agent/api/logging.py:18-20` | `_ensure_handle_dir()` | Already creates `{data_dir}/handles/{handle_id}/` — reuse this path pattern |
| `src/l4l/sub_agent/config.py:406-411` | `get_data_dir()` | Returns `Path(server.data_dir)`, creates dir. Default: `.l4l` |
| `src/l4l/sub_agent/schemas.py:231-264` | `HandleState` | Pydantic model with `model_dump_json()` — serialization ready |
| `tests/sub_agent/test_sub_agent_service.py:48-56` | `_clean_handle_storage` fixture | Monkeypatches `state._handles = {}` — must remain compatible |

### Mismatches / Notes

- `logging.py` imports `get_data_dir` from config but `state.py` currently does not. The rewrite will need to add this import.
- `_ensure_handle_dir()` in `logging.py` is not exported (underscore prefix). Options: (a) duplicate the 3-line function in `state.py`, (b) make it public, (c) import it as internal. Recommend (a) — keep `state.py` self-contained with its own `_handle_state_path()` helper.
- `app.py` needs to be checked for existing startup hooks — if none exist, the lifespan pattern must be added. This is a minor scope addition not in the phase doc but required for "load on startup" to work.
- **Forward-compatibility note**: Phase 2 adds optional fields to `HandleState` (e.g., `eb_approved: bool`). Pydantic's `model_validate_json()` handles missing optional fields with defaults, so Phase 1's persistence code will deserialize Phase 2 state files correctly without changes. No special handling needed.
