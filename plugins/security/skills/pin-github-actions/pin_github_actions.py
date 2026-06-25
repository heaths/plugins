#!/usr/bin/env python3
"""Pin GitHub Actions to exact commit SHAs with version comments.

Usage:
    pin_github_actions.py [workflow-file ...]

If no files are given, all *.yml and *.yaml files under .github/workflows/ are
processed. Run this script from the root of the repository whose workflows you
want to update.
"""

import re
import subprocess
import sys
from pathlib import Path


# Matches "uses:" lines including any leading "- " list marker.
# Groups: (1) prefix, (2) action ref, (3) @ref, (4) trailing comment
USES_RE = re.compile(
    r'^([ \t]*(?:-[ \t]+)?uses:[ \t]+)'
    r'([^\s@]+)'
    r'@([0-9a-f]{40}|[^\s#\n]+)'
    r'([ \t]*(?:#[^\n]*)?)',
    re.MULTILINE,
)

SHA_RE = re.compile(r'^[0-9a-f]{40}$')

_sha_cache: dict[tuple[str, str], str | None] = {}
_tag_cache: dict[tuple[str, str, str], str] = {}


def _run_ls_remote(repo_url: str, *patterns: str) -> str | None:
    result = subprocess.run(
        ["git", "ls-remote", repo_url, *patterns],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout if result.returncode == 0 else None


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


def _pin_match(m: re.Match) -> str:
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
            return m.group(0)  # no version comment; cannot re-resolve
        version = stripped.lstrip("#").strip()
        new_sha = resolve_to_sha(repo_url, version)
        if not new_sha:
            return m.group(0)
        exact_tag = find_exact_tag(repo_url, version, new_sha)
        return f"{prefix}{action}@{new_sha} # {exact_tag}"
    else:
        sha = resolve_to_sha(repo_url, ref)
        if not sha:
            print(f"  Warning: could not resolve {action}@{ref}", file=sys.stderr)
            return m.group(0)
        exact_tag = find_exact_tag(repo_url, ref, sha)
        return f"{prefix}{action}@{sha} # {exact_tag}"


def pin_workflow(path: Path) -> bool:
    """Pin all GitHub Actions in a workflow file. Returns True if the file changed."""
    original = path.read_text(encoding="utf-8")
    updated = USES_RE.sub(_pin_match, original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


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
    for p in paths:
        if not p.exists():
            print(f"Skipping (not found): {p}", file=sys.stderr)
            continue
        print(f"Processing {p} ...", end=" ", flush=True)
        if pin_workflow(p):
            print("updated")
            changed += 1
        else:
            print("no changes")

    print(f"\n{changed} file(s) updated.")


if __name__ == "__main__":
    main()
