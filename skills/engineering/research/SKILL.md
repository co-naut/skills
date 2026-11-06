---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

From the primary session, use `subagent` with `agent: "general"` and `background: true` to do the research, so you keep working while it reads. Start it with a fresh context window and include the question, output location, and the three steps below in its brief. The worker writes a file, so OpenCode's read-only `explore` agent is not suitable.

If you are already a child session, perform the research and write the findings yourself. Do not delegate again: OpenCode's built-in `general` child cannot launch subagents. When the background worker finishes, use its completion notification rather than polling, and spot-check its citations before relaying its claims.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
