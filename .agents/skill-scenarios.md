# Skill workflow checks

Use these scenarios after changing a listed skill or merging upstream. Inspect the installed instructions and their references first. For a live agent check, use a fresh session against a disposable repository and provide the scenario's constraints. Record whether the result is a static walkthrough, a tool-level check, or an observed agent run; one does not prove another.

| Scenario | Expected behavior |
| --- | --- |
| Setup with only `CLAUDE.md`, plus `origin` and `upstream` | Proposes `AGENTS.md`, preserves the Claude file, and confirms the exact tracker repository. |
| Setup with `AGENTS.md` symlinked to `CLAUDE.md` | Names the resolved target before editing and preserves the symlink. |
| WIP containing an interim commit, staged edits, unstaged edits, and a new untracked file | `implement` supplies its start SHA; review includes all four sources and excludes identified pre-existing work. |
| Staged review with additional unstaged edits in the same file | Review uses index contents, not the newer working-tree contents. |
| Review in a repository with no first commit | Index, working tree, and untracked files are accounted for without requiring `HEAD` to resolve. |
| `tdd` inside a worker with approved seams in its brief | Starts the loop at those seams without asking again. A changed seam returns to the parent. |
| Design-it-twice or architecture exploration in a built-in `general` child | Works directly or returns an explicit request for parent dispatch; does not attempt nested delegation. |
| Two independent implementation tickets finish together | Implementers remain isolated; only one merge writes the integration worktree at a time. New readiness comes from landed, verified tickets. |
| Worker starts on an unexpected base, or has dirty/untracked files at cleanup | Reports the state; no reset or forced removal. Only owned, clean, integrated worktrees qualify for cleanup. |
| Wayfinder has blocked and ready research tickets | Claims and dispatches only ready tickets; separate outputs or worktrees; primary publishes and updates the map serially. |
| Local tracker with no remote | Research findings gain a durable local path; no unconditional push. |
| CodeGraph tool exists but this repository is unindexed | Uses source inspection directly; no indexing side effect. |
| CodeGraph result is capped or has no edge for a suspected runtime call | Follows up through source; reports limits rather than exact global counts or proof of independence. |
| Plan-mode glossary update or HTML architecture report | Keeps proposals in the conversation until the user switches agents. |
| Session boundary with useful reasoning but little context capacity | Describes compaction as continuing the same session; `/new` as a separate session with the old history still available. |

For the Git review cases, verify the commands in the installed `code-review/REVIEW-SCOPE.md` against disposable fixtures. For orchestration cases, a static walkthrough checks that the instructions cover the branch; only a live run can verify model behavior and the current agent permissions.
