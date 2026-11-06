# OpenCode V2 fork

This is co-naut's personal OpenCode fork of [mattpocock/skills](https://github.com/mattpocock/skills). Preserve the upstream collection, docs, attribution, and plugin metadata so upstream changes can be merged. Only the paths in [opencode-skills.txt](opencode-skills.txt) belong to this fork's installed subset. A new upstream skill is not an installation request.

## Install and update

From this repository, preview the selected copies and then apply:

```sh
python scripts/install-opencode-skills.py
python scripts/install-opencode-skills.py --apply
```

The destination is `~/.agents/skills`, which V2 discovers automatically. The installer copies supporting files too. It never touches `~/.claude/skills`, removes unselected skills, or deletes extra installed files. Existing symlinks are refused rather than followed or replaced. Keep the shared `.venv`, `node_modules`, and skills installed from other sources intact.

On first adoption, or after an installed copy has been edited, the preview labels differing files `LOCAL DIFFERENCE`. Review them before running `--apply --accept-local-changes`. Every replaced file is backed up beneath `${XDG_STATE_HOME:-~/.local/state}/skills-custom/backup-*` before any installation writes. Restore a file manually from that backup if needed. Later runs use per-file hashes in that state directory to distinguish upstream updates from installed edits. A missing installed file is recreated; keep permanent customizations in this fork rather than editing deployed copies.

The installer is separate from upstream's `scripts/link-skills.sh`. That development script targets multiple harnesses and can delete conflicting directories. Do not use it for this setup.

## Merge upstream

`origin` is `git@github.com:co-naut/skills.git`. `upstream` is `https://github.com/mattpocock/skills.git`. Git remotes are local configuration; on a fresh clone, add `upstream` once:

```sh
git remote add upstream https://github.com/mattpocock/skills.git
```

With local work committed or otherwise safely preserved, fetch and merge deliberately:

```sh
git fetch upstream
git remote show upstream
git merge upstream/main
python -m unittest discover -s tests -p 'test_*.py'
python scripts/install-opencode-skills.py
python scripts/install-opencode-skills.py --apply
```

Check the default branch reported by `git remote show upstream` before merging; substitute it if it is not `main`. Resolve conflicts in the fork before installing. Keep the selection file unchanged unless intentionally changing what is installed. If upstream renames or removes a selected path, installation fails before writing; review the replacement rather than silently adding or dropping skills.

## V2 conventions

- Type `@skill-id` to load a skill. Upstream's `/skill-name` labels describe the same skills, not registered OpenCode slash commands. Keep real built-in commands distinct from skill IDs.
- OpenCode supports the retained `disable-model-invocation: true` frontmatter. For new OpenCode-only skills, prefer `metadata: {opencode/autoinvoke: false}`. Both hide automatic discovery, not explicit loading. `agents/openai.yaml` is preserved upstream metadata, not OpenCode configuration.
- The advertised skill list excludes hidden skills. It is not an installed-skill inventory. Explicit `skill` calls take `{"id":"skill-id"}` and can load hidden skills when permissions allow.
- Launch fresh child sessions with `subagent`. Use `explore` for read-only discovery and `general` for work that writes notes or code. Use a configured `reviewer` only when available; otherwise use `general` with a read-only review brief. Background work reports completion automatically; do not poll.
- A built-in `general` child cannot launch further subagents. Give it a self-contained task. If a delegated skill needs another worker, the primary agent dispatches that worker, or the child performs the task directly.
- Use `/new` for a separate session and `/sessions` to return to the old one. Compaction is lossy and continues the same session; preserve file pointers for decisions that must survive it.
- Plan mode is read-only for normal project files. When a skill needs to write code, notes, specs, or tickets, ask the user to switch to a write-capable agent rather than working around Plan restrictions through shell commands or children.

Sources: [V2 skills](https://opencode.ai/v2/docs/skills), [V2 agents](https://opencode.ai/v2/docs/agents).

## Local maintenance

Keep changes focused on selected skills and these OpenCode-specific files. The upstream catalogs and Claude plugin continue describing upstream's promoted set; they are not this fork's install manifest. Re-sync human-facing docs and `ask-matt` when changing the behavior or flow of a selected skill. Retain existing compatible frontmatter rather than rewriting every skill just for syntax.

Validate the installer with `python -m unittest discover -s tests -p 'test_*.py'`. Tests use temporary repositories and destinations, never the real installed skills. For workflow changes, use [skill-scenarios.md](skill-scenarios.md); distinguish a static instruction walkthrough from an observed agent run.
