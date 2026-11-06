# Pin the review scope

Run these commands in the repository or worktree being reviewed. Resolve refs to SHAs before dispatching fresh reviewers; include the absolute directory in each brief. Scope determines both the diff and which version of each file supplies context.

## Choose the scope

| Request | Base and diff | File context |
| --- | --- | --- |
| Branch or PR | Resolve head and target refs, then `git merge-base <target-sha> <head-sha>`. Review `git diff <base-sha> <head-sha> --`. | Read files at `<head-sha>`, not dirty working copies. |
| Since an exact commit or implementation start | Resolve that exact base and head. Review `git diff <base-sha> <head-sha> --`. | Read files at `<head-sha>`. |
| Staged changes | Resolve `HEAD`; review `git diff --cached <head-sha> --`. | Read the index version with `git show :<path>`. |
| Current uncommitted work | Resolve `HEAD`; review `git diff <head-sha> --`, plus in-scope untracked files. | Read working-tree files. |
| Implementation including interim commits and uncommitted work | Use the recorded start SHA; review `git diff <start-sha> --`, plus in-scope untracked files. | Read working-tree files. |

`git diff <sha> --` includes the net staged and unstaged changes against that base. It excludes untracked files. Use `git status --short` and `git ls-files --others --exclude-standard` to enumerate those separately, then read every in-scope untracked file. For unusual filenames, use the `-z` forms and a NUL-aware reader. A new file staged with `git add` is already in the tracked diff.

For a repository without a first commit, use `git diff --cached --` for the index, `git diff --` for unstaged changes, and the untracked listing. State that there is no committed baseline; account for the final version of every included file.

## Build the packet

- **Intent**: scope, requirements, and explicit exclusions.
- **Location**: absolute worktree path, base and head SHAs where they exist, and the exact commands.
- **Changes**: diff, changed-file list, and included untracked file contents or accessible snapshot paths. Include `git log <base-sha>..<head-sha> --oneline` when the scope includes commits.
- **Existing work**: separate pre-existing user changes from this task using the caller's starting status and diff. When changes share a file, identify relevant hunks; ask if ownership cannot be established.

Both reviewers receive the same packet. A working-tree review should use a captured diff and file snapshots when writes may continue; store snapshots under the environment's preferred temporary directory. Otherwise keep the checkout stable for the review. A child can read files the parent names, but it does not inherit the parent's conversation.

An empty tracked diff is not an empty review when in-scope untracked files exist. Only report "nothing to review" after checking the whole selected scope.
