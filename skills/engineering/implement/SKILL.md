---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Before editing, record the absolute worktree path, starting `HEAD` SHA (or that the repository has no commits), and the starting status and diff. These establish the review base and distinguish existing user work from this task.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Resolve minor ambiguity with reversible assumptions within the agreed scope. State assumptions that affect the result. Ask when a decision would change the scope or agreed behavior, when no safe next step remains, or before a hard-to-reverse action the user has not approved.

Call the Skill tool with "tdd" where possible, at pre-agreed seams.

When the repository has a CodeGraph index, explore the symbols you will change before editing, passing the absolute worktree path as `projectPath` and `maxFiles: 3`. Use its source and discovered callers; follow up capped or missing results with targeted source inspection. Without an index, read and search directly. Record unresolved caller coverage rather than claiming the graph is exhaustive.

Before adding a helper or replacing shared logic, inspect the nearest existing implementation and its callers. Reuse it when it fits, and preserve behavior outside the requested change.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, call the Skill tool with "code-review". Supply the recorded start SHA, requirements, and scope: this task's interim commits, staged and unstaged changes, and new untracked files. Identify pre-existing changes separately. Fix confirmed findings and run the relevant checks.

Before reporting completion, account for each acceptance criterion with a verification result or an explicit gap. Run any remaining checks you can within scope before reporting a gap.

Commit only when the user or project workflow authorizes it, staging this task's changes without sweeping in unrelated work. Otherwise leave the reviewed changes uncommitted and report their status.
