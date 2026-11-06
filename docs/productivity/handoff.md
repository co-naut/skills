## What it does

`handoff` writes a portable account of work in progress so a separate session can continue. It references existing specs, decisions, and diffs rather than copying them into another document.

## When to reach for it

Load `@handoff` when work needs to move to another session, directory, or person. It is hidden from automatic discovery. Continue in the current session when the reasoning still fits; compaction makes room in that same session when necessary.

## Common questions

**Where is the file?**

The skill reports a unique path under the environment's preferred temporary directory, `/tmp/opencode` in this setup. Attach it to a new session opened in the recorded working directory. Temporary files are not durable archives; preserve the file elsewhere if it must survive cleanup.

**What does the next session need?**

The handoff includes the absolute directory, branch and worktree, relevant uncommitted files, decisions, verification results, and next action. It names suggested skills and links to existing artifacts. Sensitive values are redacted.

**Can it write the file in Plan mode?**

Normal handoff-file writes wait for a write-capable agent. In Plan mode the handoff stays in the conversation, unless you explicitly request a file within OpenCode's allowed plan directory.

**How is this different from a new session or compaction?**

`/new` starts a separate session without the current task context; the old one remains accessible. Compaction summarizes older messages within the same session. A handoff is a file you can carry into another session. Neither a summary nor a handoff changes that session's permissions.

## It's working if

- The next session knows where to work and which files contain the unfinished changes.
- It can locate decisions and verification evidence without repeating discovery.
- It knows what to do next and which decisions still need you.

## Where it fits

Use it across session boundaries, including a separate [prototype](https://aihero.dev/skills-prototype) investigation. [ask-matt](https://aihero.dev/skills-ask-matt) helps choose between continuing, starting fresh, handing off, delegating, and compacting.
