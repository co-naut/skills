## What it does

`code-review` checks a pinned change set on two axes: **Standards**, whether it follows the repository's rules, and **Spec**, whether it implements the requested behavior. Findings stay separate so success on one axis cannot hide failure on the other.

## When to reach for it

Load `@code-review`, or let the agent reach for it when you request a review. Name the scope: branch or PR, changes since an exact commit, staged changes, or current work in progress. If the scope is ambiguous, it asks before reviewing.

## What gets reviewed

| Scope | Source |
| --- | --- |
| Branch or PR | Changes from the target's merge-base to the pinned head |
| Since an exact commit | Changes from that commit to the pinned head |
| Staged | Index diff and index file contents |
| WIP | Working-tree diff against the chosen base, plus relevant untracked files |

Both reviewers receive the same packet: location, SHAs, diff, included files, requirements, and exclusions. Existing unrelated user work is identified separately. A changing checkout needs captured file versions so the reviewers do not inspect different states.

The primary session launches fresh reviewers through OpenCode's `subagent` tool. A built-in `general` child performs both axes directly if this skill is loaded inside it, since it cannot launch further children. The parent verifies findings against their cited evidence.

## Common questions

**Does it see uncommitted and new files?**

Yes, when WIP is the requested scope. Tracked changes come from the working-tree diff; untracked files are enumerated and read separately. An empty tracked diff does not mean there is nothing to review.

**Do I need an issue tracker?**

Only to fetch a spec recorded there. A spec file or requirements from the conversation work directly. Without requirements, the Spec report says so instead of inventing them.

**Does CodeGraph prove the full impact?**

No. The reviewer uses indexed callers when available, follows up incomplete results through source inspection, and reports remaining coverage limits.

**Should I rerun until there are no findings?**

Fix confirmed findings and run the relevant checks. Repeat broader review when new changes or unresolved concerns justify it, not merely to chase a different set of stylistic suggestions.

## It's working if

- You can identify exactly which committed, staged, or working-tree state was reviewed.
- New untracked files are accounted for when they belong to the scope.
- Every finding cites source and a rule, smell, or requirement; unverified claims are marked.
- Standards and Spec remain separate, including the closing counts and worst issue per axis.

## Where it fits

[implement](https://aihero.dev/skills-implement) calls it before any authorized commit, passing the task's starting point and WIP. [implement-spec](https://aihero.dev/skills-implement-spec) calls it over the final integration branch. For workflow selection, use [ask-matt](https://aihero.dev/skills-ask-matt).
