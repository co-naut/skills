# Model-invoked vs user-invoked

In this OpenCode V2 fork, invocation controls **discovery**, not access:

- **User-invoked**: hidden from automatic discovery. Keep existing `disable-model-invocation: true`; for new OpenCode-only skills use `metadata: {opencode/autoinvoke: false}`. The description is a human-facing summary.
- **Model-invoked**: advertised when it has a description and permissions allow. Omit the hiding flags and write a model-facing description naming the distinct trigger branches.

Humans load either kind with `@skill-id`. The `skill` tool can explicitly load either kind by ID, including hidden skills. Permissions still apply. The advertised list is not an installed-skill inventory.

Preserve upstream `agents/openai.yaml` metadata for merges; OpenCode does not use it. See [opencode.md](opencode.md) for this fork's selected install set.

## Dependencies between them

Express an operative dependency as **call the `skill` tool with `{"id":"grilling"}`**. One skill per call; a step needing two skills names two calls. Shared reference files live with the skill that owns them, reached through that skill rather than cross-folder paths.

A router recommends `@skill-id` and stops when its workflow says to. Hidden status does not enforce that boundary. A setup step that needs human choices should tell the user to load `@setup-matt-pocock-skills`; explicit tool loading is technically possible but would start a separate setup workflow.

## Passive vs active domain work

Merely _reading_ `GLOSSARY.md` for vocabulary is a one-line prose pointer, not the `domain-modeling` skill. Only the active build/sharpen discipline (challenge terms, edge-case scenarios, write ADRs, update `GLOSSARY.md` inline) is `domain-modeling`.
