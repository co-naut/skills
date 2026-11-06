## What it does

`ask-matt` recommends a **flow** through this fork's installed skills. It reads a skill's instructions before making claims about it, then names the next step and stops. It is a router, not an orchestrator that starts the whole flow for you.

## When to reach for it

Load `@ask-matt` when you know the situation but not which skill fits. It is hidden from automatic discovery.

| Situation | Likely route |
| --- | --- |
| An idea that needs sharpening | `@grill-with-docs`, or `@grill-me` without a workspace |
| Agreed requirements that need building | `@implement`, or spec and tickets before `@implement-spec` |
| Incoming issues | `@triage` |
| A hard bug | `@diagnosing-bugs` |
| An effort too uncertain for one session | `@wayfinder` |
| Architectural friction | `@improve-codebase-architecture` |

## Common questions

**It says a hidden skill is missing. Is it?**

Not necessarily. OpenCode's advertised list omits hidden skills. The installed files and this fork's selection manifest are the evidence; explicit loading by ID still works when permissions allow.

**Should I start a new session or compact?**

Continue when the current reasoning matters and capacity permits. `/new` creates a separate session; `/sessions` returns to the old one. Compaction summarizes older context within the same session. Use `@handoff` when a separate session needs a portable account of the work. The router's phase-boundary reference explains that choice.

**Does setup have to run before everything?**

Only workflows that need missing tracker or domain configuration require it. Local review can use a supplied spec or requirements without a tracker. In Plan mode, discussing a flow does not authorize its file or tracker writes.

**Can I customize the recommendation?**

Yes. Change the skill in this fork and update its installed copy through the fork's installer. Keep standing project preferences in `AGENTS.md`. The router covers this collection; it does not automatically catalog skills from other sources.

## It's working if

- It names an actionable `@skill-id` and explains the relevant choice briefly.
- It reads a skill before recommending that you skip it.
- It distinguishes a fresh session, compaction, and a handoff.
- It recommends a flow without starting the work on your behalf.

## Where it fits

This is the entry point when you are unsure which workflow fits. The main chain runs through [grill-with-docs](https://aihero.dev/skills-grill-with-docs), [to-spec](https://aihero.dev/skills-to-spec), [to-tickets](https://aihero.dev/skills-to-tickets), and either [implement](https://aihero.dev/skills-implement) or [implement-spec](https://aihero.dev/skills-implement-spec), followed by review and retrospective.
