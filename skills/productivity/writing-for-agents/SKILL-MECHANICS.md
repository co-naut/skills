# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill (frontmatter, the invocation choice, and router skills). Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation

Two choices, trading the two loads:

- A **model-invoked** skill keeps a `description`, so the agent can fire it autonomously, and other skills can reach it. You can still type its name: model-invocation always _includes_ user reach; a description only ever adds agent discovery, never removes the human's. The description is the skill's top-level context pointer, forced to stay loaded at all times: permanent context load in exchange for discoverability. A model-invoked skill whose content is all reference is also one home for shared reference: another skill can invoke it, so reference needed by several skills lives in one place. Mechanics: omit `disable-model-invocation`, and write a model-facing description carrying the trigger branches (the pointer-writing rules in `SKILL.md` apply in full).
- In **OpenCode V2**, a **user-invoked** skill hides its description from automatic discovery. Humans load it with `@skill-id`; another skill can still load it explicitly using `skill({"id":"skill-id"})` when permissions allow. It spends cognitive load: you are the index that must remember it exists. Mechanics: set `metadata: {opencode/autoinvoke: false}`. Existing `disable-model-invocation: true` is also supported; if both are present, `opencode/autoinvoke` wins. The `description` becomes human-facing: a one-line summary, trigger lists stripped. `agents/openai.yaml` does not control OpenCode invocation.

Pick model-invocation only when the agent must discover the skill on its own. An explicit dependency from another skill can load it by ID without advertising it. If it only fires by hand or through an explicit dependency, hide it from automatic discovery and pay no description context load.

Shared reference that two user-invoked skills both need can live in a skill explicitly loaded by ID, or in a plain file reached through a context pointer. Automatic discovery is not required for explicit dependencies.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a model-invoked skill when you have a distinct leading word that should trigger it on its own (a trigger word you actually use in your prompts). You pay context load for the advertised description, so that independent discovery has to be worth it. Reuse through an explicit skill ID does not require automatic discovery.

## Router skills

When user-invoked skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**: one user-invoked skill that names the others and when to reach for each, so the human has one skill to remember instead of many. A recommendation-only router stops after naming the next `@skill-id`; that is a workflow choice, not an OpenCode restriction on loading hidden skills.
