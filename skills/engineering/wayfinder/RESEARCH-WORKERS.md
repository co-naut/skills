# Research workers

The primary session owns ticket claims, publication, and map updates. A built-in `general` child cannot orchestrate more workers; it returns required dispatches to its parent.

## Dispatch

1. Claim only an unblocked, unclaimed research ticket. Give a fresh `general` child the question, source constraints, relevant tracker context, and an absolute, unique output path under the environment's preferred temporary directory (`/tmp/opencode` here).
2. The child calls the `skill` tool with `research` and performs the research directly. Its brief limits writes to its assigned output; it returns the file path, cited findings, and unresolved questions. It neither switches branches in the shared checkout nor edits the shared map.
3. If the investigation needs code changes or a committed artifact, create a fresh `research/<name>` branch in its own worktree first. Pass its absolute path and base SHA, and require every file and shell operation to use that directory. A branch name alone does not isolate concurrent work. Unexpected dirty state or the wrong base is a blocker, not permission to reset.

## Publish and resolve

Use completion notifications. Spot-check citations and decide whether the question is answered before closing the ticket. An inconclusive investigation stays open with its findings and blocker recorded.

Publication follows the configured tracker:

- **Local files:** copy the completed findings into a durable location under `.scratch/<effort>/`, then update the ticket and map through the tracker convention. A temporary path alone is not a durable resolution link.
- **Remote tracker:** attach the findings, post the answer, or link a committed artifact using the confirmed repository. Push a research branch only when the user or project workflow authorizes that publication. Otherwise retain it locally and report the pending publication; do not present a local-only branch as a remotely accessible source.

Update resolutions and the map one at a time, rereading the latest map before each edit to preserve other sessions' decisions. Recompute the research frontier after each resolution. Retain any worktree with dirty or unpublished work; remove only clean worktrees created by this run after their artifacts have a durable home.
