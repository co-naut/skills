---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Ask Matt

Recommend a **flow**, the path through the installed skills that fits the user's situation. Read a skill's installed `SKILL.md` before stating what it does or recommending that a step be skipped. Hidden skills are absent from OpenCode's advertised list; that is not evidence they are missing. Recommend the next `@skill-id` and stop rather than starting its work.

## Main flow: idea → ship

1. **`@grill-with-docs`** sharpens an idea in a working directory, retaining terms in a glossary and decisions in ADRs. Without a workspace, use the stateless **`@grill-me`**. Both use **`@grilling`**; the difference is persistence. In Plan mode, discuss proposed records and defer project writes until the user switches agents.
2. **Does a question need a runnable answer?** Use **`@prototype`** to explore logic or UI. Use **`@handoff`** if the experiment needs a separate session or directory, then bring its findings back. Otherwise continue in the same session.
3. **Does the build span sessions?**
   - **Yes:** **`@to-spec`** synthesizes the agreed requirements and testing seams. **`@to-tickets`** splits the spec into vertical slices with blocking edges. Then choose one of the build paths below.
   - **No:** use **`@implement`** directly with the agreed requirements.

| Build path | When to use it |
| --- | --- |
| **`@implement`** per ticket | You want to steer each ticket. Start a new session for each self-contained ticket, working blockers first. It reviews the task's committed and uncommitted work against its recorded starting point. |
| **`@implement-spec`** | You want the primary session to orchestrate the whole graph. Approve seams before dispatch; workers implement in isolated worktrees, merges are serial, and one final review covers the integration branch. |

Both build paths use **`@tdd`** at approved seams and **`@code-review`** for separate Standards and Spec findings. Use either directly for a smaller task: test-first work, or review of a branch, staged changes, or WIP. Committing and publishing follow the authorized workflow.

4. **`@pr`** shapes a pull-request body when one is needed: the smallest useful visual, before/after evidence, and reversibility.
5. **`@retro`** reviews the session's process and environment after the build. Run it while the relevant history is available, or identify a prior OpenCode session for export. Mechanical mistakes suggest checks; judgement failures suggest standards or better context pointers.

## On-ramps

| Situation | Route |
| --- | --- |
| Incoming issues or external PRs need evaluation | **`@triage`**, then **`@implement`** when a brief is ready. Tickets already produced by `@to-tickets` need no extra triage. |
| A hard bug or performance regression | **`@diagnosing-bugs`** builds a tight reproduction loop, tests hypotheses, and verifies a fix. Use **`@retro`** afterward if the process exposed an environment gap. |
| The effort is too uncertain to specify in one session | **`@wayfinder`** maps decision tickets, resolving decisions rather than delivering the project. Ready research runs in isolated workers. When the map clears, use **`@to-spec`** to consolidate decisions before ticketing. |
| Architectural friction makes change or testing hard | **`@improve-codebase-architecture`** surveys likely high-value areas. Pick a candidate to explore; use **`@codebase-design`** for its interface and testing seams. |

## Shared references

- **`@domain-modeling`** challenges fuzzy terms and records glossary entries and significant decisions. Reading an existing glossary alone needs no skill invocation.
- **`@codebase-design`** defines module, interface, depth, seam, adapter, leverage, and locality. Its design-it-twice reference compares alternative interfaces; a child without delegation develops alternatives directly and reports that limitation.
- **`@writing-for-agents`** guides edits to skills, instruction files, and other agent-facing text.

CodeGraph is an environment tool, not a skill. Use it for indexed repositories, pass the worktree path explicitly, and treat partial results as partial evidence. Relevant workflows supplement it with source inspection where coverage is incomplete.

## Standalone tools

- **`@research`** gathers primary sources into a cited Markdown file. A primary session dispatches one background worker; an existing child researches directly.
- **`@to-questionnaire`** interviews the user about what they need from someone else, then writes that person's questionnaire.
- **`@wizard`** produces an interactive script for steps only a human can perform, such as dashboard setup or credential entry.
- **`@wait-what`** re-explains the last message with the missing context and simpler language.
- **`@teach`** uses the current directory as a stateful learning workspace across sessions.

## Session boundaries

Keep the idea, spec, and ticket decisions together while context capacity permits. At a phase boundary choose between continuing, `/new`, `@handoff`, delegating a scoped task, and compaction. Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) when choosing: compaction continues the same OpenCode session, while `/new` creates a separate one.

## Setup

Use **`@setup-matt-pocock-skills`** before workflows that need an unconfigured tracker or domain-doc layout. It writes OpenCode's `AGENTS.md` and referenced configuration. Standalone local review can work from the user's requirements or a spec file without tracker setup.
