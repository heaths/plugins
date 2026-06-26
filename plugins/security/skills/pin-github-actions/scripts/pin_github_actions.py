#!/usr/bin/env python3
"""Pin GitHub Actions to exact commit SHAs with version comments.

Usage:
    pin_github_actions.py [workflow-file ...]

If no files are given, all *.yml and *.yaml files under .github/workflows/ are
processed. Run this script from the root of the repository whose workflows you
want to update.
"""

import sys

if sys.version_info < (3, 10):
    sys.exit(
        f"Python 3.10 or later is required "
        f"(found {sys.version_info.major}.{sys.version_info.minor})."
    )

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


# Matches "uses:" lines including any leading "- " list marker.
# Groups: (1) prefix, (2) action ref, (3) @ref, (4) trailing comment
# Anchored to end-of-line to prevent partial matches on unusual refs.
USES_RE = re.compile(
    r'^([ \t]*(?:-[ \t]+)?uses:[ \t]+)'
    r'([^\s@]+)'
    r'@([0-9a-f]{40}|[^\s#\n]+)'
    r'([ \t]*(?:#[^\n]*)?)$',
    re.MULTILINE,
)

SHA_RE = re.compile(r'^[0-9a-f]{40}$')

_sha_cache: dict[tuple[str, str], str | None] = {}
_tag_cache: dict[tuple[str, str, str], str] = {}


@dataclass
class PinResult:
    changed: bool = False
    unresolved: list[str] = field(default_factory=list)


def _run_ls_remote(repo_url: str, *patterns: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "ls-remote", repo_url, *patterns],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"  Warning: git ls-remote failed for {repo_url}: {e}", file=sys.stderr)
        return None


def _resolve_tag(repo_url: str, tag: str) -> str | None:
    output = _run_ls_remote(repo_url, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}")
    if not output:
        return None
    sha = None
    for line in output.splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        if parts[1] == f"refs/tags/{tag}^{{}}":
            sha = parts[0]  # prefer dereferenced SHA (annotated tag)
        elif parts[1] == f"refs/tags/{tag}" and sha is None:
            sha = parts[0]  # lightweight tag fallback
    return sha


def _resolve_branch(repo_url: str, branch: str) -> str | None:
    output = _run_ls_remote(repo_url, f"refs/heads/{branch}")
    if not output or not output.strip():
        return None
    parts = output.split("\t", 1)
    return parts[0] if len(parts) == 2 else None


def resolve_to_sha(repo_url: str, ref: str) -> str | None:
    """Resolve a tag or branch name to a commit SHA, with caching."""
    key = (repo_url, ref)
    if key not in _sha_cache:
        _sha_cache[key] = _resolve_tag(repo_url, ref) or _resolve_branch(repo_url, ref)
    return _sha_cache[key]


def find_exact_tag(repo_url: str, ref: str, sha: str) -> str:
    """Return the highest matching semver tag that resolves to sha.

    Queries all tags under the same major prefix (e.g. "v4.*" for ref "v4" or
    "v4.1.0"). Falls back to ref if no match is found.
    """
    key = (repo_url, ref, sha)
    if key in _tag_cache:
        return _tag_cache[key]

    major = ref.split(".")[0]  # "v4" from "v4" or "v4.1.0"
    output = _run_ls_remote(repo_url, f"refs/tags/{major}.*")
    if not output:
        _tag_cache[key] = ref
        return ref

    # Build map of tag -> sha, preferring dereferenced (annotated) SHAs
    tags: dict[str, str] = {}
    for line in output.splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        line_sha, refname = parts
        tag = refname.removeprefix("refs/tags/")
        if tag.endswith("^{}"):
            tags[tag[:-3]] = line_sha
        elif tag not in tags:
            tags[tag] = line_sha

    matching = [t for t, s in tags.items() if s == sha]
    if not matching:
        _tag_cache[key] = ref
        return ref

    def semver_key(t: str) -> tuple[int, ...]:
        try:
            return tuple(int(p) for p in t.lstrip("v").split("."))
        except ValueError:
            return (0,)

    best = max(matching, key=semver_key)
    _tag_cache[key] = best
    return best


def _pin_match(path: Path, unresolved: list[str], m: re.Match) -> str:
    """Return a pinned replacement for a single uses: regex match."""
    prefix = m.group(1)
    action = m.group(2)
    ref = m.group(3)
    comment = m.group(4)

    # Skip local workflow references and Docker image references
    if action.startswith(".") or "://" in action:
        return m.group(0)

    repo = "/".join(action.split("/")[:2])
    repo_url = f"https://github.com/{repo}.git"

    if SHA_RE.match(ref):
        # Already pinned to a SHA — re-resolve using the version in the comment
        stripped = comment.strip()
        if not stripped.startswith("#"):
            unresolved.append(
                f"{path}: {action}@{ref} is pinned to a SHA but missing a version comment"
            )
            return m.group(0)
        version = stripped.lstrip("#").strip()
        new_sha = resolve_to_sha(repo_url, version)
        if not new_sha:
            unresolved.append(f"{path}: could not re-resolve {action} from comment {version}")
            return m.group(0)
        exact_tag = find_exact_tag(repo_url, version, new_sha)
        return f"{prefix}{action}@{new_sha} # {exact_tag}"
    else:
        sha = resolve_to_sha(repo_url, ref)
        if not sha:
            unresolved.append(f"{path}: could not resolve {action}@{ref}")
            return m.group(0)
        exact_tag = find_exact_tag(repo_url, ref, sha)
        return f"{prefix}{action}@{sha} # {exact_tag}"


def pin_workflow(path: Path) -> PinResult:
    """Pin all GitHub Actions in a workflow file."""
    original = path.read_text(encoding="utf-8")
    unresolved: list[str] = []
    updated = USES_RE.sub(lambda m: _pin_match(path, unresolved, m), original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return PinResult(changed=True, unresolved=unresolved)
    return PinResult(unresolved=unresolved)


def main() -> None:
    args = sys.argv[1:]
    if args:
        paths = [Path(a) for a in args]
    else:
        wf_dir = Path(".github/workflows")
        if not wf_dir.is_dir():
            sys.exit("No .github/workflows directory found.")
        paths = sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml"))

    if not paths:
        sys.exit("No workflow files found.")

    changed = 0
    unresolved_count = 0
    for p in paths:
        if not p.exists():
            print(f"Skipping (not found): {p}", file=sys.stderr)
            unresolved_count += 1
            continue
        print(f"Processing {p} ...", end=" ", flush=True)
        result = pin_workflow(p)
        if result.changed:
            print("updated")
            changed += 1
        elif result.unresolved:
            print("needs attention")
        else:
            print("no changes")
        for warning in result.unresolved:
            print(f"  Warning: {warning}", file=sys.stderr)
        unresolved_count += len(result.unresolved)

    print(f"\n{changed} file(s) updated.")
    if unresolved_count:
        sys.exit(f"{unresolved_count} reference(s) still need manual attention.")


if __name__ == "__main__":
    main()
