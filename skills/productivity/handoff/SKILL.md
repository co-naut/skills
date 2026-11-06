---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Use a unique file in the environment's preferred temporary directory (`/tmp/opencode` here), otherwise `$TMPDIR` or the OS temp directory. In Plan mode, present the handoff in the conversation; write an OpenCode plan file only when the user explicitly requests one within the allowed plan directory.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Include the absolute working directory, branch and worktree, relevant uncommitted files, outstanding decisions, verification results, and the next action. Tell the user to start a new session in that directory and attach the handoff file. A handoff preserves task context, not permissions to resume writes from Plan mode.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
