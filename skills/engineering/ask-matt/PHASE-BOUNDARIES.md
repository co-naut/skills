# Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the implementation, the QA. The definition is fuzzy on purpose: a phase ends when you think *"ok, we're done with that"*.

The **phase boundary** is the gap between two phases, and it is the only place this decision belongs. Mid-phase there is no decision to make: continue, or split the work that's left into subagents. Compacting mid-phase makes the agent lose the thread.

## The five options

| Option       | What it does                                                    |
| ------------ | --------------------------------------------------------------- |
| **Continue** | Stay in the session. No context switch at all.                    |
| **`/new`** | Start a separate session; the old one remains available.          |
| **`@handoff`** | Write a portable markdown file for a new session.               |
| **Subagent** | Send the task to its own context window and get a report back.     |
| **Compact** | Summarize older context and continue in the same session.        |

## The tree

Work top to bottom at the boundary. The first **yes** wins.

**1. Can you continue in this session?** Continue when the next phase needs the reasoning verbatim and there is enough context capacity for the work. Judge capacity against the selected model and current usage, not a universal token threshold. Grilling → implementation is the standard case. Preserve references to settled decisions before automatic compaction becomes necessary.

**2. Is the context irrelevant to what comes next?** Start a new OpenCode session with **`/new`**. Supply the ticket or other context the next task needs. The old session stays available through `/sessions`.

The new session does not know the **why** behind prior decisions until you provide it. Return to the old session or pass a handoff when that reasoning matters.

**3. Do you need to hand off?** Use `@handoff` when you are:

- continuing in a **separate session** that needs a portable account of the work,
- moving to a **new directory** or repo,
- sending the work to a **colleague**,
- or forking a side task you found **mid-phase** without derailing what you're doing.

What `@handoff` buys is **portability**: a file that travels. If the same session can continue, prefer that to a handoff.

**4. Can the task be done AFK?** Is it scoped tightly enough to run with you away from the keyboard, no steering? Then send it to a **subagent** and leave this session untouched. Automated review is the standard case: the agent reads the diff and reports, and you aren't needed while it does.

**5. Otherwise, compact.** OpenCode V2 summarizes older conversation and retains recent context in the same session. Earlier messages stay stored. State the next phase and durable decision pointers before requesting compaction through the available UI action; consult the V2 compaction docs for API automation rather than inventing slash-command arguments.

Compaction is the **default, not the first reach**. It sits at the bottom because the four questions above it are cheaper or more precise. The failure mode is continuing confidently from a summary that flattened a decision.

## Primary and secondary sources

Compaction and handoff use **secondary sources**: summaries of what happened. They can lose reasoning even though the original session remains stored. A child also sees only the brief and sources you provide, not the parent's whole conversation.

| Source                            | Information | Noise | Room to move |
| --------------------------------- | ----------- | ----- | ------------ |
| Primary (Continue)                | Full        | Lots  | Little       |
| Secondary (compaction, handoff) | Lossy       | Less  | Lots         |

This is why question 1 comes first. You only pay the lossiness when staying costs more than it saves.

## These are judgement calls

The questions are not objective: each has taste in it, and the same boundary can go two ways on two days. The value is in asking them **in order**, at the boundary rather than in the middle of the work.
