#!/usr/bin/env python3
"""Preview or copy only this fork's selected skills, preserving local edits."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


REPO = Path(__file__).resolve().parent.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(content)
            stream.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def install(args):
    destination = args.destination.expanduser().absolute()
    if destination.is_symlink():
        raise ValueError(f"destination must not be a symlink: {destination}")
    destination = destination.resolve()
    if destination == REPO or REPO in destination.parents or destination in REPO.parents:
        raise ValueError("destination must be separate from this repository")

    state_dir = args.state_dir.expanduser().resolve()
    if state_dir == destination or destination in state_dir.parents:
        raise ValueError("state directory must be outside the skills destination")
    key = hashlib.sha256(str(destination).encode()).hexdigest()[:16]
    state_file = state_dir / f"{key}.json"
    previous = json.loads(state_file.read_text()) if state_file.exists() else {}
    if previous and (previous["destination"] != str(destination) or previous["repository"] != str(REPO)):
        raise ValueError("state belongs to another destination or repository")
    previous_hashes = previous.get("files", {})

    files = {}
    names = set()
    for line in (REPO / ".agents/opencode-skills.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        source = REPO / line
        if not source.resolve().is_relative_to(REPO / "skills") or not (source / "SKILL.md").is_file():
            raise ValueError(f"invalid skill path: {line}")
        if source.name in names:
            raise ValueError(f"duplicate skill ID: {source.name}")
        names.add(source.name)
        target = destination / source.name
        if target.is_symlink() or (target.exists() and not target.is_dir()):
            raise ValueError(f"skill destination must be a real directory: {target}")
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"source symlinks are not supported: {path}")
            if path.is_file():
                relative = Path(source.name) / path.relative_to(source)
                files[relative.as_posix()] = path
    if not names:
        raise ValueError("skill selection is empty")

    changes = []
    conflicts = []
    for relative, source in files.items():
        target = destination / relative
        for component in (target, *target.parents):
            if component == destination:
                break
            if component.is_symlink():
                raise ValueError(f"refusing symlink in destination: {component}")
            if component != target and component.exists() and not component.is_dir():
                raise ValueError(f"parent is not a directory: {component}")
        if target.exists() and not target.is_file():
            raise ValueError(f"file destination is not a regular file: {target}")
        current = digest(target) if target.exists() else None
        if current == digest(source):
            continue
        changes.append(relative)
        if current is not None and previous_hashes.get(relative) != current:
            conflicts.append(relative)

    print(f"Selected {len(names)} skills; {len(changes)} changed files.")
    for relative in changes:
        label = "LOCAL DIFFERENCE" if relative in conflicts else "UPDATE"
        print(f"{label}: {relative}")
    if conflicts and not args.accept_local_changes:
        if args.apply:
            raise ValueError("local differences found; review the preview, then use --accept-local-changes to back up and replace them")
        print("Apply would refuse local differences without --accept-local-changes.")
    if not args.apply:
        print("Preview only. Pass --apply to install; unselected skills and extra files are never removed.")
        return

    existing = [relative for relative in changes if (destination / relative).exists()]
    if existing:
        state_dir.mkdir(parents=True, exist_ok=True)
        backup = Path(tempfile.mkdtemp(prefix="backup-", dir=state_dir))
        for relative in existing:
            saved = backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destination / relative, saved)
        print(f"Backed up replaced files to {backup}")

    for relative in changes:
        source = files[relative]
        target = destination / relative
        atomic_write(target, source.read_bytes())
        shutil.copymode(source, target)
    state = {
        "destination": str(destination),
        "repository": str(REPO),
        "files": {relative: digest(destination / relative) for relative in files},
    }
    atomic_write(state_file, (json.dumps(state, indent=2) + "\n").encode())
    print(f"Installed {len(names)} skills into {destination}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=Path.home() / ".agents/skills")
    parser.add_argument("--state-dir", type=Path, default=Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")) / "skills-custom")
    parser.add_argument("--apply", action="store_true", help="write changes (default: preview only)")
    parser.add_argument("--accept-local-changes", action="store_true", help="back up and replace reviewed local differences")
    args = parser.parse_args()
    try:
        install(args)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
