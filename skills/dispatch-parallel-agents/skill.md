---
name: dispatch-parallel-agents
description: Dispatch independent tasks to parallel subagents when 2+ problems can be solved without shared state or sequential dependencies.
license: MIT
compatibility:
  opencode: ">=0.1"
metadata:
  category: execution
  phase: implementation
---

# Skill: Dispatch Parallel Agents

This skill parallelizes independent work across multiple subagents. Each agent gets a focused scope, isolated context, and a clear deliverable.

---

## When to Use

Use when:

- 2+ independent tasks exist that do not share state
- Each task can be understood and completed without context from the others
- Tasks do not edit the same files

Do **not** use when:

- Failures are related (fixing one might fix others -- investigate together first)
- Tasks require understanding the full system state
- Agents would interfere with each other (editing the same files, using the same resources)
- You are in exploratory mode and do not yet know what is broken

---

## Execution Model

### Roles

- **Primary (coordinator)**
  - Identifies independent problem domains
  - Crafts focused prompts for each agent
  - Reviews results and integrates changes
  - Resolves conflicts if agents touched overlapping code

- **Subagents (workers)**
  - Each receives a scoped task with all necessary context
  - Works independently without knowledge of other agents
  - Returns a summary of findings and changes

---

## Workflow

### Step 1: Identify Independent Domains

Group tasks by what they affect. Each domain must be independent -- fixing one must not affect the others.

Example:
- Domain A: Fix stats page header styling
- Domain B: Update billing page layout
- Domain C: Add admin role detection

These are independent because they touch different files and different logic.

### Step 2: Craft Agent Prompts

Each agent prompt must be:

- **Focused** -- one clear problem domain, not "fix everything"
- **Self-contained** -- all context needed to understand the problem (file paths, error messages, expected behavior)
- **Constrained** -- explicit boundaries on what the agent should and should not change
- **Output-specific** -- what the agent should return (summary, file list, verification result)

### Step 3: Dispatch

Launch all agents in a single message with multiple Agent tool calls. This ensures true parallel execution.

### Step 4: Review and Integrate

When agents return:

1. Read each agent's summary
2. Check for conflicts (did agents edit the same code?)
3. Verify changes work together (run build, run tests)
4. Integrate all changes

---

## Rules

1. **Independence is mandatory**: If tasks share state or files, do not parallelize. Process sequentially instead.
2. **Focused prompts**: Each agent gets exactly what it needs. Do not dump full session context into agent prompts.
3. **Verify after integration**: Always run the build and relevant tests after merging all agent outputs. Agents cannot verify cross-agent interactions.
4. **Do not over-parallelize**: 2-3 agents is typical. More than 5 agents indicates the tasks should be structured differently (e.g., as a plan with phases).
5. **Conflicts require manual resolution**: If two agents edited the same file, the primary resolves the conflict -- do not blindly apply both changes.
