---
name: implement-spec
description: "Implement the result of @to-spec and @to-tickets in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to load `@setup-matt-pocock-skills`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Start every subagent with a fresh context window.

Run orchestration in the primary session. If invoked in a child, return the task graph and required dispatches to the parent. Use OpenCode's `subagent` tool with `general` for workers that write files; `explore` is read-only. Built-in `general` children cannot launch more subagents. Completion notifications drive background work.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and tickets to understand the task graph. Confirm test seams in the primary session unless the spec already records approval. Pass the approved seams and acceptance criteria to each worker; a changed seam returns to the parent for a decision.

2. (optional) Use a `general` exploration worker to write shared notes under the environment's preferred temporary directory (`/tmp/opencode` here). Give future workers the absolute path. Use absolute or tracker references for tickets that are untracked and therefore absent from new worktrees.

3. Record the starting commit and checkout status. Create a fresh integration branch and worktree from the agreed base, preserving existing user changes. Record every branch and worktree this run owns. If the tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge, using the confirmed remote and target branch.

4. For each ready ticket, create a fresh branch and worktree from the current integration tip, then dispatch a fresh `general` **implementer subagent**. Include the absolute worktree path, base SHA, ticket, approved seams, relevant project instructions, and verification commands. Child sessions do not gain worktree isolation automatically. Each worker:
   - verifies its directory, branch, base, and clean starting status; reports unexpected state instead of resetting;
   - uses the assigned directory for every file and shell operation;
   - calls the `skill` tool with `tdd`, using the supplied seam approval;
   - commits only its ticket's changes on its assigned branch;
   - reports commit SHA, test commands and results, skipped checks, blockers, and any unresolved changes. Unavailable fixtures or environment dependencies are reported, not counted as passing tests.

5. Merge completed tickets **one at a time** in the integration worktree. A `general` merger receives that absolute path and the worker's commit SHA. Confirm a clean integration worktree, merge the ticket, and run checks appropriate to the combined changes. Resolve conflicts against the spec; escalate ambiguous decisions. Mark a ticket landed only after the merge and checks succeed. The merge queue is serial even while implementers run in parallel.

6. Recompute the **frontier** from successfully landed tickets, not tracker closure: a PR-based tracker may keep them open until the final PR merges. Dispatch newly ready tickets from the updated integration tip.

7. Once all tickets have landed, call the `skill` tool with `code-review`, passing the integration worktree, exact starting and final SHAs, and the full spec. Fix confirmed findings in a fresh implementer worktree, merge through the same queue, and run focused checks for the findings plus integration checks. Broaden review only for new changes or unresolved concerns.

8. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work, and report the integration branch.

9. Remove only worktrees recorded as owned by this run, after their workers finish, their commits are included in the integration branch, and their status is clean including untracked files. Use non-forced removal; retain and report dirty or unmerged worktrees. Keep the integration branch and report where its result can be inspected.
