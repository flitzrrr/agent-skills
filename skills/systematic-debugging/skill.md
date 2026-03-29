---
name: systematic-debugging
description: Investigate bugs, test failures, and unexpected behavior through root-cause analysis before proposing fixes. Use when encountering any technical issue.
license: MIT
compatibility:
  opencode: ">=0.1"
metadata:
  category: debugging
  phase: investigation
---

# Skill: Systematic Debugging

This skill enforces root-cause investigation before any fix attempt. Random fixes waste time and create new bugs.

---

## When to Use

Use for any technical issue:

- Test failures
- Bugs in production or development
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

Do **not** skip this skill when:

- The issue seems simple (simple bugs have root causes too)
- You are under time pressure (systematic debugging is faster than thrashing)
- A fix seems obvious (obvious fixes often mask the real problem)

---

## Execution Model

- **Primary agent** runs this skill directly.
- **Rationale**: Debugging requires iterative investigation in the same context. Delegating to a subagent loses the accumulated understanding.
- **Exception**: For multi-component issues spanning independent subsystems, delegate per-subsystem investigation to separate agents via the `dispatch-parallel-agents` skill.

---

## Workflow

### Phase 1: Root Cause Investigation

**No fixes are allowed until this phase is complete.**

1. **Read error messages carefully** -- stack traces, line numbers, error codes. Do not skip past them.
2. **Reproduce consistently** -- determine the exact steps. If not reproducible, gather more data instead of guessing.
3. **Check recent changes** -- `git diff`, recent commits, new dependencies, config changes, environmental differences.
4. **Gather evidence at component boundaries** -- for multi-layer systems (CI -> build -> deploy, API -> service -> database), add diagnostic logging at each boundary to identify where the failure occurs.
5. **Trace data flow** -- follow the bad value backward through the call stack to its origin. Fix at the source, not at the symptom.

### Phase 2: Pattern Analysis

1. **Find working examples** -- locate similar working code in the same codebase.
2. **Compare against references** -- if implementing a pattern, read the reference implementation completely. Do not skim.
3. **Identify differences** -- list every difference between working and broken code, however small.
4. **Understand dependencies** -- what components, settings, config, and environment does this code need?

### Phase 3: Hypothesis and Testing

1. **Form a single hypothesis** -- state clearly: "I think X is the root cause because Y."
2. **Test minimally** -- make the smallest possible change to test the hypothesis. One variable at a time.
3. **Verify before continuing** -- if the hypothesis is wrong, form a new one. Do not stack fixes.
4. **Acknowledge unknowns** -- if you do not understand something, say so. Do not pretend.

### Phase 4: Implementation

1. **Fix the root cause, not the symptom.**
2. **One change at a time** -- no "while I'm here" improvements, no bundled refactoring.
3. **Verify the fix** -- run the relevant tests, confirm the issue is resolved, confirm no regressions.
4. **If 3+ fixes have failed** -- stop. The issue is likely architectural, not a bug. Discuss with the user before attempting more fixes.

---

## Rules

1. **No fixes without investigation**: Phase 1 must be complete before proposing any fix.
2. **One hypothesis at a time**: Do not apply multiple changes simultaneously.
3. **Evidence over intuition**: Every fix must be justified by evidence from the investigation, not by "it might work."
4. **Escalate after 3 failed attempts**: Three failed fixes indicate an architectural problem. Stop fixing and discuss with the user.
5. **Do not increase timeouts as a fix**: Find the real timing issue instead.
6. **Read error messages completely**: Stack traces contain the answer more often than not.
