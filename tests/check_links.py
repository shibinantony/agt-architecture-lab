"""Check public documentation links; network checks are explicitly opt-in.

Usage:
    python tests/check_links.py
    python tests/check_links.py --list-external
    python tests/check_links.py --external --workers 4 --timeout 10

Uses only the standard library. Local checks cover repository Markdown links,
heading fragments, explicit HTML anchors, and root-relative contract references.
External checks establish HTTP reachability, not the accuracy of source content.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {
    ".git", ".agents", ".codex", ".gemini", ".local-conversation",
    ".conversations", ".chat-history", ".pytest_cache", "__pycache__",
    "node_modules", "artifacts", "out", "reports", "evidence",
}
INLINE_LINK = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?P<target><[^>\n]+>|[^\s)]+)"
    r"(?:\s+['\"][^\n]*?['\"])?\s*\)"
)
REFERENCE_DEFINITION = re.compile(
    r"^ {0,3}\[(?P<label>[^\]\n]+)\]:\s*(?P<target><[^>\n]+>|\S+)", re.MULTILINE
)
REFERENCE_LINK = re.compile(r"!?\[(?P<label>[^\]\n]+)\]\[(?P<reference>[^\]\n]*)\]")
AUTOLINK = re.compile(r"<(https?://[^>\s]+)>")
HTML_LINK = re.compile(r"\bhref\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
HTML_ANCHOR = re.compile(r"\b(?:id|name)\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
ATX_HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
CONTRACT_PATH = re.compile(r"^(?:[\w.-]+/)+[^\s?#]+(?:#[^\s]+)?$")


@dataclass(frozen=True)
class Link:
    source: Path
    line: int
    target: str
    root_relative: bool = False

    def location(self) -> str:
        return f"{self.source.relative_to(ROOT).as_posix()}:{self.line}"


def public_files():
    for directory, names, files in os.walk(ROOT):
        names[:] = sorted(
            name for name in names
            if name not in EXCLUDED
            and not name.startswith(".venv")
            and not (Path(directory) / name).is_symlink()
        )
        for name in sorted(files):
            path = Path(directory) / name
            if not path.is_symlink() and path.suffix.lower() in {".md", ".json"}:
                yield path


def without_fences(text: str) -> str:
    """Hide fenced examples while preserving line numbers for diagnostics."""
    result = []
    fence_character = ""
    fence_length = 0
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if not fence_character and match:
            fence_character, fence_length = match[1][0], len(match[1])
            result.append("\n" if line.endswith("\n") else "")
        elif fence_character:
            if match and match[1][0] == fence_character and len(match[1]) >= fence_length:
                fence_character = ""
            result.append("\n" if line.endswith("\n") else "")
        else:
            result.append(line)
    return "".join(result)


def heading_anchors(text: str) -> set[str]:
    text = without_fences(text)
    anchors = set(HTML_ANCHOR.findall(text))
    duplicates: Counter[str] = Counter()
    for match in ATX_HEADING.finditer(text):
        label = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", match[1])
        label = html.unescape(re.sub(r"<[^>]+>", "", label)).lower()
        slug = re.sub(r"[^\w\- ]", "", label).replace(" ", "-")
        suffix = duplicates[slug]
        duplicates[slug] += 1
        anchors.add(f"{slug}-{suffix}" if suffix else slug)
    return anchors


def markdown_links(path: Path, text: str) -> list[Link]:
    text = without_fences(text)
    links = []
    definitions = {
        match["label"].casefold(): match["target"]
        for match in REFERENCE_DEFINITION.finditer(text)
    }
    for pattern in (INLINE_LINK, REFERENCE_DEFINITION):
        for match in pattern.finditer(text):
            links.append(Link(path, text.count("\n", 0, match.start()) + 1, match["target"].strip("<>")))
    for pattern in (AUTOLINK, HTML_LINK):
        for match in pattern.finditer(text):
            links.append(Link(path, text.count("\n", 0, match.start()) + 1, match[1]))
    for match in REFERENCE_LINK.finditer(text):
        reference = (match["reference"] or match["label"]).casefold()
        if reference in definitions:
            links.append(Link(path, text.count("\n", 0, match.start()) + 1, definitions[reference].strip("<>")))
        else:
            links.append(Link(path, text.count("\n", 0, match.start()) + 1, f"missing-reference:{reference}"))
    return links


def contract_links(path: Path, text: str) -> list[Link]:
    """The decision-contract reference fields use repository-root-relative paths."""
    if path.parent != ROOT / "framework" / "templates":
        return []
    value = json.loads(text)
    links = []

    def visit(node):
        if isinstance(node, dict):
            for key, item in node.items():
                if key in {"reference", "definition_reference"} and isinstance(item, str):
                    if item.startswith(("https://", "http://")) or CONTRACT_PATH.fullmatch(item):
                        position = text.find(json.dumps(item))
                        links.append(Link(path, text.count("\n", 0, max(position, 0)) + 1, item, True))
                visit(item)
        elif isinstance(node, list):
            for item in node:
                visit(item)

    visit(value)
    return links


def check_local(link: Link, contents: dict[Path, str]) -> str | None:
    target = html.unescape(link.target)
    if target.startswith("missing-reference:"):
        return f"undefined Markdown reference {target.split(':', 1)[1]!r}"
    parsed = urllib.parse.urlsplit(target)
    if parsed.scheme in {"http", "https", "mailto"}:
        return None
    if parsed.scheme or parsed.netloc:
        return f"unsupported link scheme: {target}"
    base = ROOT if link.root_relative or parsed.path.startswith("/") else link.source.parent
    path = (base / urllib.parse.unquote(parsed.path).lstrip("/")).resolve() if parsed.path else link.source
    try:
        path.relative_to(ROOT)
    except ValueError:
        return f"link leaves repository: {target}"
    if not path.exists():
        return f"missing local target: {target}"
    if parsed.fragment:
        fragment = urllib.parse.unquote(parsed.fragment)
        if path.is_dir():
            path /= "README.md"
        if path.suffix.lower() == ".md" and path.is_file():
            text = contents.get(path)
            if text is None:
                text = path.read_text(encoding="utf-8")
            if fragment not in heading_anchors(text):
                return f"missing heading/HTML anchor: {target}"
        elif not re.fullmatch(r"L\d+(?:-L\d+)?", fragment):
            return f"cannot resolve fragment on non-Markdown target: {target}"
    return None


def check_external(url: str, timeout: float) -> tuple[str, str, str]:
    # Read response headers only; do not download entire documents or assets.
    request = urllib.request.Request(url, headers={"User-Agent": "agt-architecture-lab-link-check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            return url, "ok", f"HTTP {status}"
    except urllib.error.HTTPError as exc:
        kind = "error" if exc.code in {404, 410} else "warning"
        return url, kind, f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return url, "warning", f"unverified: {type(exc).__name__}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--external", action="store_true", help="Also check public HTTP(S) URLs; performs network requests")
    parser.add_argument("--list-external", action="store_true", help="List unique external URLs without accessing the network")
    parser.add_argument("--external-host", action="append", default=[], help="Limit network checks to this exact host; repeatable")
    parser.add_argument("--workers", type=int, default=4, choices=range(1, 9), metavar="1..8")
    parser.add_argument("--timeout", type=float, default=10, help="Per-request timeout in seconds, between 1 and 30")
    parser.add_argument("--strict-external", action="store_true", help="Treat inaccessible/rate-limited external URLs as failures")
    args = parser.parse_args(argv)
    if not 1 <= args.timeout <= 30:
        parser.error("--timeout must be between 1 and 30 seconds")
    contents = {}
    links = []
    errors = 0
    markdown_count = 0
    for path in public_files():
        try:
            text = path.read_text(encoding="utf-8")
            contents[path.resolve()] = text
            if path.suffix.lower() == ".md":
                markdown_count += 1
                links.extend(markdown_links(path, text))
            else:
                links.extend(contract_links(path, text))
        except (UnicodeError, OSError, json.JSONDecodeError) as exc:
            errors += 1
            print(f"ERROR {path.relative_to(ROOT)}: {exc}")
    external = {}
    local_count = 0
    for link in links:
        url = urllib.parse.urlsplit(html.unescape(link.target))
        if url.scheme in {"http", "https"}:
            canonical = urllib.parse.urlunsplit(url._replace(fragment=""))
            external.setdefault(canonical, []).append(link.location())
        else:
            local_count += 1
            problem = check_local(link, contents)
            if problem:
                errors += 1
                print(f"ERROR {link.location()}: {problem}")
    if args.list_external:
        for url in sorted(external):
            print(url)
    warnings = 0
    checked = 0
    if args.external:
        urls = sorted(url for url in external if not args.external_host or urllib.parse.urlsplit(url).hostname in args.external_host)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(check_external, url, args.timeout) for url in urls]
            for future in concurrent.futures.as_completed(futures):
                url, kind, message = future.result()
                checked += 1
                if kind == "error":
                    errors += 1
                if kind == "warning":
                    warnings += 1
                if kind != "ok":
                    print(f"{kind.upper()} {external[url][0]}: {message}: {url}")
    print(f"Checked {markdown_count} Markdown files, {local_count} local links/fragments, {checked}/{len(external)} unique external URLs; {errors} errors, {warnings} warnings.")
    if not args.external:
        print("Network checks not run; add --external to verify HTTP reachability.")
    return 1 if errors or (args.strict_external and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
