---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

- **Facts:** Look up what you can verify. Inspect directly for quick checks; for longer read-only exploration, dispatch a fresh OpenCode `explore` subagent when available and permitted. Otherwise inspect directly. While research is pending, ask the ready questions that don't depend on it.
- **Defaults:** Carry forward minor, reversible choices that leave scope, user-facing or agreed behavior, and constraints intact. Put defaults that affect the plan in the recap rather than asking about each one.
- **Decisions:** Ask the user about meaningful tradeoffs, changes to scope or user-facing behavior, and hard-to-reverse commitments. Wait for their answer. Use the `question` tool for choices when it fits the round; otherwise ask in the conversation.

An empty frontier can mean the remaining branches are blocked. Close only when every in-scope branch is settled or the user has explicitly deferred it. Recap the decisions, defaults that affect the plan, and deferrals, then ask the user to confirm the shared understanding. Confirmation closes the interview; implementing the plan requires separate authorization.
