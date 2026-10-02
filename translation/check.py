#!/usr/bin/env python3
"""Prüft die deutsche Übersetzung gegen den Basis-Commit.

Benötigt Python >= 3.11 sowie `markdown-it-py` und `mdit-py-plugins`:

    pip install markdown-it-py==3.0.0 mdit-py-plugins

Aufrufe:

    translation/check.py [check] [DATEIEN...]   Strukturprüfung (Standard: alle
                                                gegenüber der Basis geänderten
                                                Dateien; --all für alle)
    translation/check.py review [DATEIEN...]    Review-Grep auf erzwungene
                                                Übersetzungen von Rust-Begriffen
    translation/check.py english [DATEIEN...]   sucht übrig gebliebene englische
                                                Absätze außerhalb von Code
    translation/check.py gen-heading-ids --html DIR
                                                erzeugt heading-ids.json aus
                                                einem HTML-Build des Basis-Commits
    translation/check.py restore-ws [DATEIEN...] stellt Leerzeichen am Zeilenende
                                                wieder her, die Editoren in
                                                Codezeilen entfernt haben
    translation/check.py verify-html --html DIR [--base-html DIR]
                                                prüft, ob ein HTML-Build alle
                                                alten Überschriften-IDs und
                                                Sprungziele enthält

Optionen:

    --base REV                Basis-Revision (Standard: BASE_COMMIT)
    --comments keep|translate-inline
                              keep: Code bleibt byte-identisch (Standard).
                              translate-inline: Kommentare in Rust-Codeblöcken
                              direkt in .md-Dateien dürfen sich unterscheiden.

Fehler (ERROR) führen zu Exit-Code 1, Warnungen (WARN) nicht.
"""

from __future__ import annotations

import difflib
import fnmatch
import json
import re
import subprocess
import sys
import tomllib
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

try:
    from markdown_it import MarkdownIt
    from markdown_it.token import Token
    from mdit_py_plugins.footnote import footnote_plugin
except ImportError:  # pragma: no cover
    sys.exit(
        "check.py braucht markdown-it-py und mdit-py-plugins:\n"
        "    pip install markdown-it-py==3.0.0 mdit-py-plugins"
    )

REPO = Path(__file__).resolve().parent.parent
BASE_COMMIT = "88250e0392cef0622f318e35469108d68694c1f7"
HEADING_IDS = REPO / "translation" / "heading-ids.json"
EXCEPTIONS = REPO / "translation" / "check-exceptions.toml"

# Only these paths may differ from the base commit.
ALLOWED_CHANGES = [
    re.compile(p)
    for p in (
        r"^src/[^/]+\.md$",
        r"^quizzes/[^/]+\.toml$",
        r"^book\.toml$",
        r"^translation/",
    )
]

# The translator's note on the first page is excluded from the comparison.
TRANSLATOR_NOTE_RE = re.compile(
    r"<!-- de:translator-note:start -->.*?<!-- de:translator-note:end -->\n*",
    re.S,
)

HEADING_ATTR_RE = re.compile(r"\s*\{#([A-Za-z0-9_\-]+)\}\s*$")
DIRECTIVE_RE = re.compile(r"\{\{#.*?\}\}")
PERM_RE = re.compile(r"@Perm(?:\[[^\]]*\])?\{[^}]*\}")
URL_RE = re.compile(r"https?://[^\s<>)\]\"'`\x00]*[^\s<>)\]\"'`\x00.,;:!?]")
TRANSLATABLE_ATTRS = {"alt", "title", "caption"}
CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1", re.S)
REF_DEF_RE = re.compile(r"^ {0,3}\[(?!\^)[^\]]+\]:\s")

REVIEW_WORDS = [
    "Eigenschaft",
    "Merkmal",
    "Kiste",
    "Struktur",
    "Aufzählung",
    "Abschluss",
    "Lebensdauer",
    "Eigentümer",
    "Ausleihprüfer",
    "Stapelspeicher",
    "Haldenspeicher",
    "Zeichenkette",
    "Panik",
    "Muster",
    "intelligenter Zeiger",
    "intelligente Zeiger",
]

# First use of these German terms on each page should carry the English term,
# e.g. "verschoben (*moved*)". Checked as a warning only.
GLOSS_TERMS = [
    (re.compile(r"\b(verschieb\w*|verschob\w*|verschiebt)\b", re.I), "move"),
    (re.compile(r"\b(ausgeliehen\w*|ausleih\w*|auszuleihen)\b", re.I), "borrow"),
    (re.compile(r"\bGültigkeitsbereich\w*"), "scope"),
    (re.compile(r"\b(verworfen\w*|verwerf\w*|verwirft)\b", re.I), "drop"),
    (re.compile(r"(?<![Uu]n)\bveränderlich(?!keit)\w*"), "mutable"),
    (re.compile(r"\bunveränderlich(?!keit)\w*", re.I), "immutable"),
]

ENGLISH_WORDS = set(
    """the and of to is are that this with for you we be can not by or from
    have has which when would should your our they there their what how does
    it its into than then these those were was been being here only also
    just because while however""".split()
)
WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß']+")


# --------------------------------------------------------------------------
# Reporting


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"ERROR {where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"WARN  {where}: {msg}")


# --------------------------------------------------------------------------
# Git helpers


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout


def base_text(path: str, base: str) -> str | None:
    try:
        return git("show", f"{base}:{path}")
    except subprocess.CalledProcessError:
        return None


def changed_files(base: str) -> list[str]:
    tracked = git("diff", "--name-only", base).split("\n")
    untracked = git("ls-files", "--others", "--exclude-standard").split("\n")
    return sorted({p for p in tracked + untracked if p})


# --------------------------------------------------------------------------
# Exceptions


def load_exceptions() -> dict[str, Any]:
    if EXCEPTIONS.exists():
        return tomllib.loads(EXCEPTIONS.read_text())
    return {}


def allowed(kind: str, path: str, text: str, exceptions: dict[str, Any]) -> bool:
    for entry in exceptions.get(kind, []):
        if not fnmatch.fnmatch(path, entry.get("file", "*")):
            continue
        if "word" in entry and entry["word"] in text:
            return True
        if "contains" in entry and entry["contains"] in text:
            return True
    return False


# --------------------------------------------------------------------------
# Markdown analysis


def make_md() -> MarkdownIt:
    return (
        MarkdownIt("commonmark", {"html": True})
        .enable(["table", "strikethrough"])
        .use(footnote_plugin)
    )


MD = make_md()


class HtmlScan(HTMLParser):
    """Collects tags (with non-translatable attributes) and text from HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[tuple] = []
        self.translatable: list[str] = []
        self.text: list[str] = []

    def _attrs(self, attrs: list[tuple[str, str | None]]) -> tuple:
        out = []
        for name, value in attrs:
            if name in TRANSLATABLE_ATTRS:
                self.translatable.append(value or "")
                out.append((name, "<translatable>"))
            else:
                out.append((name, value))
        return tuple(out)

    def handle_starttag(self, tag, attrs):
        self.items.append(("start", tag, self._attrs(attrs)))

    def handle_startendtag(self, tag, attrs):
        self.items.append(("startend", tag, self._attrs(attrs)))

    def handle_endtag(self, tag):
        self.items.append(("end", tag))

    def handle_comment(self, data):
        # Line wrapping may move a line break inside a comment such as
        # "<!-- ignore -->"; only the words matter.
        self.items.append(("comment", " ".join(data.split())))

    def handle_data(self, data):
        self.text.append(data)


RAW_TAG_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9-]*)")


@dataclass
class HtmlInfo:
    items: list[tuple]
    raw_tags: list[str]
    translatable: list[str]
    text: str


def scan_html(html: str) -> HtmlInfo:
    scanner = HtmlScan()
    scanner.feed(html)
    scanner.close()
    # Tag names exactly as written (HTMLParser lowercases them, but the
    # trpl-listing preprocessor matches `<Listing` case-sensitively).
    raw_tags = [
        m.group(0)
        for m in RAW_TAG_RE.finditer(re.sub(r"<!--.*?-->", "", html, flags=re.S))
    ]
    return HtmlInfo(scanner.items, raw_tags, scanner.translatable, "".join(scanner.text))


def code_spans(text: str) -> Counter:
    return Counter(m.group(2).strip() for m in CODE_SPAN_RE.finditer(text))


@dataclass
class InlineInfo:
    code: Counter
    hrefs: Counter
    images: Counter
    html: Counter
    footnotes: Counter
    directives: list[str]
    perms: Counter
    urls: Counter
    emphasis: int
    strong: int
    text: str  # prose only (no code, no HTML)
    is_heading: bool = False


def inline_info(tok: Token, heading: bool = False) -> InlineInfo:
    code: Counter = Counter()
    hrefs: Counter = Counter()
    images: Counter = Counter()
    html: Counter = Counter()
    footnotes: Counter = Counter()
    em = strong = 0
    flat: list[str] = []
    prose: list[str] = []

    def walk(children: list[Token]) -> None:
        nonlocal em, strong
        for c in children:
            if c.type == "code_inline":
                code[c.content.strip()] += 1
                flat.append("\x00")
            elif c.type == "link_open":
                hrefs[c.attrs.get("href")] += 1
                flat.append("\x00")
            elif c.type == "image":
                images[c.attrs.get("src")] += 1
                flat.append("\x00")
                walk(c.children or [])
            elif c.type == "html_inline":
                info = scan_html(c.content)
                for item in info.items:
                    html[item] += 1
                for tag in info.raw_tags:
                    html[("raw", tag)] += 1
                for value in info.translatable:
                    for span, n in code_spans(value).items():
                        code[span] += n
                flat.append("\x00")
            elif c.type == "footnote_ref":
                footnotes[c.meta["label"]] += 1
                flat.append("\x00")
            elif c.type == "em_open":
                # A gloss like "(*moved*)" is not counted as emphasis.
                prev = flat[-1] if flat else ""
                if not prev.rstrip().endswith(("(", "(engl.")):
                    em += 1
                flat.append("\x00")
            elif c.type == "strong_open":
                strong += 1
                flat.append("\x00")
            elif c.type == "text":
                flat.append(c.content)
                prose.append(c.content)
            elif c.type in ("softbreak", "hardbreak"):
                flat.append("\n")
                prose.append(" ")
            else:
                flat.append("\x00")

    walk(tok.children or [])
    text = "".join(flat)
    if heading:
        text = HEADING_ATTR_RE.sub("", text)
    prose_text = "".join(prose)
    if heading:
        prose_text = HEADING_ATTR_RE.sub("", prose_text)
    return InlineInfo(
        code=code,
        hrefs=hrefs,
        images=images,
        html=html,
        footnotes=footnotes,
        directives=DIRECTIVE_RE.findall(text),
        perms=Counter(PERM_RE.findall(text)),
        urls=Counter(URL_RE.findall(text)),
        emphasis=em,
        strong=strong,
        text=prose_text,
        is_heading=heading,
    )


@dataclass
class Block:
    sig: tuple
    line: int
    token: Token
    inline: Token | None = None


def blocks_of(tokens: list[Token]) -> list[Block]:
    out: list[Block] = []
    last_line = 1
    for t in tokens:
        if t.map:
            last_line = t.map[0] + 1
        if t.type == "inline":
            if out:
                out[-1].inline = t
            continue
        if t.type.endswith("_close"):
            out.append(Block(("close", t.type[: -len("_close")]), last_line, t))
            continue
        if t.type == "heading_open":
            sig: tuple = ("heading", t.tag)
        elif t.type == "paragraph_open":
            sig = ("paragraph", t.hidden)
        elif t.type == "ordered_list_open":
            sig = ("ordered_list", t.attrs.get("start"))
        elif t.type in ("th_open", "td_open"):
            sig = (t.type, t.attrs.get("style"))
        else:
            sig = (t.type,)
        out.append(Block(sig, last_line, t))
    return out


def describe(sig: tuple) -> str:
    return " ".join(str(s) for s in sig)


def heading_texts(tokens: list[Token]) -> list[tuple[int, str]]:
    out = []
    for i, t in enumerate(tokens):
        if t.type == "heading_open":
            out.append((int(t.tag[1]), tokens[i + 1].content))
    return out


def ref_def_lines(text: str, tokens: list[Token]) -> list[str]:
    lines = text.split("\n")
    masked = set()
    for t in tokens:
        if t.type in ("fence", "code_block", "html_block") and t.map:
            masked.update(range(t.map[0], t.map[1]))
    return [
        line
        for i, line in enumerate(lines)
        if i not in masked and REF_DEF_RE.match(line)
    ]


def strip_rust_comments(code: str) -> list[str]:
    """Removes // and /* */ comments outside of string literals, per line."""
    out = []
    in_block = False
    for line in code.split("\n"):
        result = []
        i = 0
        in_str = False
        while i < len(line):
            ch = line[i]
            if in_block:
                if line.startswith("*/", i):
                    in_block = False
                    i += 2
                else:
                    i += 1
                continue
            if in_str:
                result.append(ch)
                if ch == "\\" and i + 1 < len(line):
                    result.append(line[i + 1])
                    i += 2
                    continue
                if ch == '"':
                    in_str = False
                i += 1
                continue
            if ch == '"':
                in_str = True
                result.append(ch)
                i += 1
                continue
            if line.startswith("//", i):
                break
            if line.startswith("/*", i):
                in_block = True
                i += 2
                continue
            result.append(ch)
            i += 1
        out.append("".join(result).rstrip())
    return out


@dataclass
class Ctx:
    report: Report
    path: str
    comments: str = "keep"
    is_md_file: bool = True


def compare_fence(ctx: Ctx, where: str, b: Token, t: Token) -> None:
    if b.info != t.info:
        ctx.report.error(where, f"Info-String geändert: {b.info!r} -> {t.info!r}")
        return
    if b.content == t.content:
        return
    lang = b.info.split(",")[0].strip()
    if (
        ctx.comments == "translate-inline"
        and ctx.is_md_file
        and lang in ("rust", "")
        and not ctx.path.startswith("listings/")
    ):
        b_lines = b.content.split("\n")
        t_lines = t.content.split("\n")
        if len(b_lines) != len(t_lines):
            ctx.report.error(where, "Codeblock: Zeilenzahl geändert")
            return
        for bl, tl in zip(b_lines, t_lines):
            if ("ANCHOR" in bl or "--snip--" in bl) and bl != tl:
                ctx.report.error(where, f"Codeblock: Marker geändert: {bl!r}")
                return
        if strip_rust_comments(b.content) == strip_rust_comments(t.content):
            return
    diff = "\n".join(
        difflib.unified_diff(
            b.content.split("\n"), t.content.split("\n"), "base", "neu", lineterm="", n=1
        )
    )
    ctx.report.error(where, f"Codeblock ({b.info or 'ohne Info'}) geändert:\n{diff}")


def compare_html(ctx: Ctx, where: str, b_html: str, t_html: str) -> InlineInfo | None:
    bi, ti = scan_html(b_html), scan_html(t_html)
    if bi.items != ti.items:
        b_set, t_set = Counter(bi.items), Counter(ti.items)
        missing = list((b_set - t_set).elements())
        extra = list((t_set - b_set).elements())
        if not missing and not extra:
            ctx.report.error(where, "HTML: Reihenfolge der Tags/Kommentare geändert")
        else:
            ctx.report.error(
                where,
                f"HTML-Tags/Attribute/Kommentare geändert; fehlt: {missing[:3]}; neu: {extra[:3]}",
            )
    if bi.raw_tags != ti.raw_tags:
        ctx.report.error(where, f"HTML-Tagnamen geändert: {bi.raw_tags} -> {ti.raw_tags}")
    b_code = code_spans(bi.text) + sum((code_spans(v) for v in bi.translatable), Counter())
    t_code = code_spans(ti.text) + sum((code_spans(v) for v in ti.translatable), Counter())
    if b_code != t_code:
        ctx.report.error(
            where,
            f"Inline-Code im HTML geändert; fehlt: {list((b_code - t_code).elements())}; "
            f"neu: {list((t_code - b_code).elements())}",
        )
    for name, rx in (("Direktiven", DIRECTIVE_RE), ("@Perm-Markup", PERM_RE)):
        if Counter(rx.findall(bi.text)) != Counter(rx.findall(ti.text)):
            ctx.report.error(where, f"{name} im HTML geändert")
    return None


def compare_inline(ctx: Ctx, where: str, b: InlineInfo, t: InlineInfo) -> None:
    def diff_counter(name: str, bc: Counter, tc: Counter) -> None:
        if bc != tc:
            missing = list((bc - tc).elements())
            extra = list((tc - bc).elements())
            ctx.report.error(where, f"{name} geändert; fehlt: {missing}; neu: {extra}")

    diff_counter("Inline-Code", b.code, t.code)
    diff_counter("Linkziele", b.hrefs, t.hrefs)
    diff_counter("Bildpfade", b.images, t.images)
    diff_counter("Inline-HTML", b.html, t.html)
    diff_counter("Fußnotenverweise", b.footnotes, t.footnotes)
    diff_counter("@Perm-Markup", b.perms, t.perms)
    diff_counter("URLs im Text", b.urls, t.urls)
    if b.directives != t.directives:
        ctx.report.error(where, f"Direktiven geändert: {b.directives} -> {t.directives}")
    if b.emphasis != t.emphasis or b.strong != t.strong:
        ctx.report.warn(
            where,
            f"Hervorhebungen: kursiv {b.emphasis}->{t.emphasis}, fett {b.strong}->{t.strong}",
        )


def compare_markdown(
    ctx: Ctx,
    base: str,
    trans: str,
    expected_ids: list[dict] | None,
    label: str,
    line_offset: int = 0,
) -> list[tuple[int, InlineInfo]]:
    """Compares two Markdown texts. Returns (line, info) for each prose block of
    the translation, for the text-based checks."""
    b_env: dict = {}
    t_env: dict = {}
    b_tokens = MD.parse(base, b_env)
    t_tokens = MD.parse(trans, t_env)
    b_blocks = blocks_of(b_tokens)
    t_blocks = blocks_of(t_tokens)
    prose: list[tuple[int, InlineInfo]] = []

    def where(line: int) -> str:
        return f"{label}:{line + line_offset}"

    # Structure: the same sequence of blocks (headings, paragraphs, lists, list
    # items, blockquotes, code blocks, HTML blocks, tables).
    b_sigs = [blk.sig for blk in b_blocks]
    t_sigs = [blk.sig for blk in t_blocks]
    if b_sigs != t_sigs:
        sm = difflib.SequenceMatcher(a=b_sigs, b=t_sigs, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            b_line = b_blocks[i1].line if i1 < len(b_blocks) else b_blocks[-1].line
            t_line = t_blocks[j1].line if j1 < len(t_blocks) else t_blocks[-1].line
            ctx.report.error(
                where(t_line),
                "Struktur weicht ab (Basis Zeile "
                f"{b_line + line_offset}): {tag}: "
                f"{[describe(s) for s in b_sigs[i1:i2]][:4]} -> "
                f"{[describe(s) for s in t_sigs[j1:j2]][:4]}",
            )
            break
        counts = lambda sigs, kind: sum(1 for s in sigs if s[0] == kind)  # noqa: E731
        for kind in ("heading", "paragraph", "list_item", "blockquote_open", "fence"):
            kb, kt = counts(b_sigs, kind), counts(t_sigs, kind)
            if kb != kt:
                ctx.report.error(where(1), f"Anzahl {kind}: {kb} -> {kt}")
        return prose

    heading_index = 0
    for bb, tb in zip(b_blocks, t_blocks):
        w = where(tb.line)
        if bb.token.type == "fence":
            compare_fence(ctx, w, bb.token, tb.token)
        elif bb.token.type == "code_block":
            if bb.token.content != tb.token.content:
                ctx.report.error(w, "eingerückter Codeblock geändert")
        elif bb.token.type == "html_block":
            compare_html(ctx, w, bb.token.content, tb.token.content)
            text = scan_html(tb.token.content).text
            prose.append((tb.line + line_offset, InlineInfo(
                Counter(), Counter(), Counter(), Counter(), Counter(), [], Counter(),
                Counter(), 0, 0, text)))
        is_heading = bb.token.type == "heading_open"
        if bb.inline is not None and tb.inline is not None:
            bi = inline_info(bb.inline, heading=is_heading)
            ti = inline_info(tb.inline, heading=is_heading)
            compare_inline(ctx, w, bi, ti)
            prose.append((tb.line + line_offset, ti))
        if is_heading:
            check_heading_id(ctx, w, bb, tb, expected_ids, heading_index)
            heading_index += 1

    # Reference definitions and footnotes.
    b_refs = {k: v["href"] for k, v in b_env.get("references", {}).items()}
    t_refs = {k: v["href"] for k, v in t_env.get("references", {}).items()}
    if b_refs != t_refs:
        ctx.report.error(where(1), "Referenz-Linkdefinitionen geändert")
    if ref_def_lines(base, b_tokens) != ref_def_lines(trans, t_tokens):
        ctx.report.error(where(1), "Referenz-Linkdefinitionen nicht byte-identisch")
    b_fn = sorted(b_env.get("footnotes", {}).get("refs", {}).keys())
    t_fn = sorted(t_env.get("footnotes", {}).get("refs", {}).keys())
    if b_fn != t_fn:
        ctx.report.error(where(1), f"Fußnoten-Labels geändert: {b_fn} -> {t_fn}")
    return prose


def check_heading_id(
    ctx: Ctx, where: str, bb: Block, tb: Block, expected: list[dict] | None, index: int
) -> None:
    if expected is None:
        return
    b_text = bb.inline.content if bb.inline else ""
    t_text = tb.inline.content if tb.inline else ""
    m = HEADING_ATTR_RE.search(t_text)
    if index >= len(expected):
        ctx.report.error(where, "Überschrift ohne Eintrag in heading-ids.json")
        return
    want = expected[index]["id"]
    if m:
        if m.group(1) != want:
            ctx.report.error(where, f"Überschriften-ID {m.group(1)!r}, erwartet {want!r}")
    elif t_text.strip() != b_text.strip():
        ctx.report.error(where, f"übersetzte Überschrift ohne ID; ergänze {{#{want}}}")


# --------------------------------------------------------------------------
# Prose checks (warnings and greps)


def gloss_warnings(ctx: Ctx, prose: list[tuple[int, InlineInfo]]) -> None:
    for rx, english in GLOSS_TERMS:
        for line, info in prose:
            if info.is_heading:
                continue
            m = rx.search(info.text)
            if not m:
                continue
            # The gloss is "(*english*)", at most a few words after the term
            # ("veränderliche Referenz (*mutable reference*)"). Emphasis
            # markers are not part of the prose text.
            gloss = re.match(r"[^()]{0,30}\(([^)]*)\)", info.text[m.end():])
            if not gloss or english not in gloss.group(1).lower():
                ctx.report.warn(
                    f"{ctx.path}:{line}",
                    f"erste Verwendung von „{m.group(0)}“ ohne Glosse (*{english}…*)",
                )
            break


def typography_warnings(ctx: Ctx, prose: list[tuple[int, InlineInfo]]) -> None:
    for line, info in prose:
        text = info.text
        where = f"{ctx.path}:{line}"
        if "—" in text:
            ctx.report.warn(where, "Geviertstrich „—“; im Deutschen „ – “ verwenden")
        if re.search(r"(?<![\w=])\"[^\"\n]+\"", text):
            ctx.report.warn(where, "gerade Anführungszeichen \"…\" im Fließtext; „…“ verwenden")
        if re.search(r"\b(z\.B\.|d\.h\.|u\.a\.)", text):
            ctx.report.warn(where, "Abkürzung ohne Leerzeichen (z. B., d. h., u. a.)")


def review_hits(path: str, prose: list[tuple[int, InlineInfo]], exceptions: dict) -> list[str]:
    hits = []
    for line, info in prose:
        for word in REVIEW_WORDS:
            for m in re.finditer(r"\w*" + re.escape(word) + r"\w*", info.text):
                found = m.group(0)
                if allowed("review_allow", path, found, exceptions):
                    continue
                start = max(0, m.start() - 40)
                hits.append(f"{path}:{line}: „{found}“ … {info.text[start: m.end() + 40]!r}")
    return hits


def english_hits(path: str, prose: list[tuple[int, InlineInfo]], exceptions: dict) -> list[str]:
    hits = []
    for line, info in prose:
        text = URL_RE.sub("", info.text)
        words = [w.lower() for w in WORD_RE.findall(text)]
        if not words:
            continue
        eng = sum(1 for w in words if w in ENGLISH_WORDS)
        if eng >= 3 and eng / len(words) >= 0.12:
            if allowed("english_allow", path, info.text, exceptions):
                continue
            hits.append(f"{path}:{line}: {eng}/{len(words)} englische Funktionswörter: {info.text[:100]!r}")
    return hits


# --------------------------------------------------------------------------
# Quiz files


QUIZ_TRANSLATABLE = {
    ("prompt", "prompt"),
    ("answer", "answer"),
    ("prompt", "distractors"),
    ("context",),
    ("answer", "alternatives"),
}
QUIZ_EXACT = {
    ("id",),
    ("type",),
    ("multipart",),
    ("prompt", "program"),
    ("answer", "stdout"),
}
LETTERS_RE = re.compile(r"[A-Za-zÄÖÜäöüß]{2,}")


def has_prose(s: str) -> bool:
    s = re.sub(r"```.*?```", "", s, flags=re.S)
    s = CODE_SPAN_RE.sub("", s)
    s = re.sub(r"<[^>]+>", "", s)
    return bool(LETTERS_RE.search(s))


def plain_len(s: str) -> int:
    s = re.sub(r"```.*?```", "", s, flags=re.S)
    return len(s.strip())


def check_quiz(ctx: Ctx, base: str, trans: str) -> list[tuple[int, InlineInfo]]:
    prose: list[tuple[int, InlineInfo]] = []
    try:
        t_data = tomllib.loads(trans)
    except tomllib.TOMLDecodeError as e:
        ctx.report.error(ctx.path, f"ungültiges TOML: {e}")
        return prose
    b_data = tomllib.loads(base)
    if set(b_data) != set(t_data):
        ctx.report.error(ctx.path, f"Top-Level-Schlüssel geändert: {set(b_data)} -> {set(t_data)}")
        return prose

    def compare_string(label: str, b: str, t: str, translatable: bool) -> None:
        if b == t:
            if translatable:
                prose.extend(
                    compare_markdown(Ctx(Report(), ctx.path, "keep", False), b, t, None, label)
                )
            return
        if not translatable or not has_prose(b):
            ctx.report.error(label, f"darf nicht geändert werden: {b[:60]!r} -> {t[:60]!r}")
            return
        prose.extend(compare_markdown(ctx, b, t, None, label))

    # Shared multipart prompts.
    if "multipart" in b_data:
        bm, tm = b_data["multipart"], t_data["multipart"]
        if set(bm) != set(tm):
            ctx.report.error(ctx.path, "multipart-Schlüssel geändert")
        for key in bm:
            if key in tm:
                compare_string(f"{ctx.path}[multipart.{key}]", bm[key], tm[key], True)

    bq, tq = b_data.get("questions", []), t_data.get("questions", [])
    if len(bq) != len(tq):
        ctx.report.error(ctx.path, f"Anzahl der Fragen: {len(bq)} -> {len(tq)}")
        return prose

    for n, (b, t) in enumerate(zip(bq, tq), 1):
        qlabel = f"{ctx.path}[Frage {n} {b.get('id', '')[:8]}]"
        qtype = b.get("type")

        def walk(bv: Any, tv: Any, path: tuple[str, ...]) -> None:
            label = f"{qlabel}.{'.'.join(path)}"
            if isinstance(bv, dict):
                if not isinstance(tv, dict):
                    ctx.report.error(label, "Typ geändert")
                    return
                extra = set(tv) - set(bv)
                if path == ("answer",) and qtype == "ShortAnswer":
                    extra -= {"alternatives"}
                if set(bv) - set(tv) or extra:
                    ctx.report.error(label, f"Schlüssel geändert: {sorted(bv)} -> {sorted(tv)}")
                for k in bv:
                    if k in tv:
                        walk(bv[k], tv[k], path + (k,))
                return
            if isinstance(bv, list):
                if not isinstance(tv, list) or len(bv) != len(tv):
                    ctx.report.error(label, "Liste: Länge oder Typ geändert")
                    return
                for i, (bi, ti) in enumerate(zip(bv, tv)):
                    walk(bi, ti, path + (str(i),))
                return
            if type(bv) is not type(tv):
                ctx.report.error(label, f"Werttyp geändert: {type(bv).__name__} -> {type(tv).__name__}")
                return
            if not isinstance(bv, str):
                if bv != tv:
                    ctx.report.error(label, f"Wert geändert: {bv!r} -> {tv!r}")
                return
            key = tuple(p for p in path if not p.isdigit())
            if qtype == "ShortAnswer" and key == ("answer", "answer") and bv != tv:
                alts = t.get("answer", {}).get("alternatives", [])
                if bv not in alts:
                    ctx.report.error(
                        label,
                        "ShortAnswer übersetzt: die englische Antwort muss in answer.alternatives bleiben",
                    )
                return
            if key in QUIZ_EXACT:
                if bv != tv:
                    ctx.report.error(label, "darf nicht geändert werden")
                return
            if key not in QUIZ_TRANSLATABLE:
                ctx.report.warn(label, "unbekanntes String-Feld, exakt verglichen")
                if bv != tv:
                    ctx.report.error(label, "geändert")
                return
            compare_string(label, bv, tv, True)

        walk(b, t, ())

        # Answer/distractor length balance (warning only).
        if qtype == "MultipleChoice":
            ba, ta = b.get("answer", {}).get("answer"), t.get("answer", {}).get("answer")
            bd, td = b.get("prompt", {}).get("distractors"), t.get("prompt", {}).get("distractors")
            if ba and bd and ta and td:
                as_list = lambda x: x if isinstance(x, list) else [x]  # noqa: E731
                avg = lambda xs: sum(plain_len(x) for x in xs) / len(xs)  # noqa: E731
                b_ratio = avg(as_list(ba)) / max(avg(bd), 1)
                t_ratio = avg(as_list(ta)) / max(avg(td), 1)
                # One-letter distractors such as "R", "W", "O" make the
                # ratio meaningless.
                if avg(bd) >= 5 and b_ratio > 0 and abs(t_ratio / b_ratio - 1) > 0.3:
                    ctx.report.warn(
                        qlabel,
                        f"Längenverhältnis Antwort/Distraktoren {b_ratio:.2f} -> {t_ratio:.2f}",
                    )
    return prose


# --------------------------------------------------------------------------
# book.toml


def check_book_toml(ctx: Ctx, base: str, trans: str) -> None:
    try:
        t = tomllib.loads(trans)
    except tomllib.TOMLDecodeError as e:
        ctx.report.error(ctx.path, f"ungültiges TOML: {e}")
        return
    b = tomllib.loads(base)
    for d in (b, t):
        d.get("book", {}).pop("title", None)
        d.get("book", {}).pop("language", None)
    if b != t:
        ctx.report.error(ctx.path, "außer book.title und book.language geändert")
    for line in difflib.ndiff(base.split("\n"), trans.split("\n")):
        if line.startswith(("+ ", "- ")) and not re.match(r"[+-] (title|language)\s*=", line):
            if line[2:].strip():
                ctx.report.error(ctx.path, f"geänderte Zeile: {line!r}")


# --------------------------------------------------------------------------
# Commands


def load_heading_ids() -> dict[str, list[dict]]:
    if HEADING_IDS.exists():
        return json.loads(HEADING_IDS.read_text())
    return {}


def analyse_file(
    path: str, base: str, comments: str, report: Report, heading_ids: dict
) -> list[tuple[int, InlineInfo]]:
    ctx = Ctx(report, path, comments, path.endswith(".md"))
    b = base_text(path, base)
    full = REPO / path
    if b is None:
        report.error(path, "Datei existiert im Basis-Commit nicht")
        return []
    if not full.exists():
        report.error(path, "Datei fehlt")
        return []
    t = full.read_text()
    if path == "book.toml":
        check_book_toml(ctx, b, t)
        return []
    if path.endswith(".toml"):
        return check_quiz(ctx, b, t)
    if path.endswith(".md"):
        # Blank out the note (keeping line numbers) instead of cutting it.
        t = TRANSLATOR_NOTE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), t)
        expected = None if path.endswith("SUMMARY.md") else heading_ids.get(path)
        if expected is None and not path.endswith("SUMMARY.md") and b != t:
            report.warn(path, "keine Einträge in heading-ids.json; IDs nicht geprüft")
        return compare_markdown(ctx, b, t, expected, path)
    return []


def select_files(args: list[str], base: str, all_files: bool) -> list[str]:
    if args:
        return [str(Path(a).resolve().relative_to(REPO)) for a in args]
    if all_files:
        files = sorted(str(p.relative_to(REPO)) for p in (REPO / "src").glob("*.md"))
        files += sorted(str(p.relative_to(REPO)) for p in (REPO / "quizzes").glob("*.toml"))
        return files + ["book.toml"]
    return [
        p
        for p in changed_files(base)
        if re.match(r"^(src/[^/]+\.md|quizzes/[^/]+\.toml|book\.toml)$", p)
    ]


def cmd_check(files: list[str], base: str, comments: str, report: Report) -> None:
    for p in changed_files(base):
        if not any(rx.match(p) for rx in ALLOWED_CHANGES):
            report.error(p, "außerhalb des erlaubten Bereichs geändert")
    heading_ids = load_heading_ids()
    for path in files:
        prose = analyse_file(path, base, comments, report, heading_ids)
        ctx = Ctx(report, path)
        if path.endswith(".md") and not path.endswith("SUMMARY.md"):
            b = base_text(path, base)
            if b is not None and (REPO / path).read_text() != b:
                gloss_warnings(ctx, prose)
                typography_warnings(ctx, prose)
        elif path.endswith(".toml") and path != "book.toml":
            b = base_text(path, base)
            if b is not None and (REPO / path).read_text() != b:
                typography_warnings(ctx, prose)


def cmd_grep(kind: str, files: list[str], base: str) -> int:
    exceptions = load_exceptions()
    heading_ids = load_heading_ids()
    hits: list[str] = []
    for path in files:
        if path == "book.toml":
            continue
        b = base_text(path, base)
        if b is not None and (REPO / path).read_text() == b:
            continue  # untranslated
        prose = analyse_file(path, base, "keep", Report(), heading_ids)
        fn = review_hits if kind == "review" else english_hits
        hits += fn(path, prose, exceptions)
    for h in hits:
        print(h)
    print(f"{len(hits)} Treffer")
    return 0


def cmd_restore_ws(files: list[str], base: str) -> int:
    """Restores trailing whitespace on lines that the base commit has with
    trailing whitespace and the translation has without (editors and tools
    often strip it, which changes code blocks). Only non-blank lines that
    occur equally often in both files are touched."""
    for path in files:
        b = base_text(path, base)
        if b is None:
            continue
        full = REPO / path
        t_lines = full.read_text().split("\n")
        b_lines = b.split("\n")
        changed = 0
        for stripped in {line.rstrip() for line in b_lines if line != line.rstrip()}:
            if not stripped.strip():
                continue
            originals = [line for line in b_lines if line.rstrip() == stripped]
            targets = [i for i, line in enumerate(t_lines) if line.rstrip() == stripped]
            if not targets:
                continue  # line was translated
            if len(originals) != len(targets):
                print(f"WARN  {path}: {stripped[:60]!r}: {len(originals)} in Basis, {len(targets)} in Übersetzung; nicht angepasst")
                continue
            for i, original in zip(targets, originals):
                if t_lines[i] != original:
                    t_lines[i] = original
                    changed += 1
        if changed:
            full.write_text("\n".join(t_lines))
            print(f"{path}: {changed} Zeilen angepasst")
    return 0


MAIN_RE = re.compile(r"<main>(.*?)</main>", re.S)
H_ID_RE = re.compile(r"<h([1-6]) id=\"([^\"]+)\"")
ANY_ID_RE = re.compile(r"\bid=\"([^\"]+)\"")
HREF_RE = re.compile(r"href=\"([^\"]*?)\"")


def cmd_gen_heading_ids(html_dir: Path, base: str) -> int:
    out: dict[str, list[dict]] = {}
    problems = 0
    for path in sorted(git("ls-tree", "--name-only", base, "src/").split()):
        if not path.endswith(".md") or path.endswith("SUMMARY.md"):
            continue
        text = base_text(path, base) or ""
        headings = heading_texts(MD.parse(text))
        page = html_dir / (Path(path).stem + ".html")
        if not page.exists():
            print(f"WARN  {path}: keine HTML-Seite {page.name}")
            continue
        main = MAIN_RE.search(page.read_text())
        ids = H_ID_RE.findall(main.group(1) if main else "")
        if len(ids) != len(headings) or any(
            int(lvl) != h[0] for (lvl, _), h in zip(ids, headings)
        ):
            print(f"ERROR {path}: {len(headings)} Überschriften, {len(ids)} IDs im HTML")
            problems += 1
            continue
        out[path] = [
            {"level": lvl, "text": text, "id": hid}
            for (lvl, text), (_, hid) in zip(headings, ids)
        ]
    HEADING_IDS.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(f"{HEADING_IDS.relative_to(REPO)}: {sum(map(len, out.values()))} IDs aus {len(out)} Seiten")
    return 1 if problems else 0


def page_ids(path: Path) -> set[str]:
    return set(ANY_ID_RE.findall(path.read_text()))


def broken_anchors(html_dir: Path) -> set[tuple[str, str]]:
    cache: dict[str, set[str]] = {}
    broken = set()
    for page in sorted(html_dir.glob("*.html")):
        if page.name in ("print.html", "404.html", "toc.html"):
            continue
        main = MAIN_RE.search(page.read_text())
        if not main:
            continue
        for href in HREF_RE.findall(main.group(1)):
            if "://" in href or href.startswith("mailto:") or "#" not in href:
                continue
            target, frag = href.split("#", 1)
            target_page = html_dir / target if target else page
            if not target_page.exists() or target_page.suffix != ".html":
                continue
            key = target_page.name
            if key not in cache:
                cache[key] = page_ids(target_page)
            if frag not in cache[key]:
                broken.add((page.name, href))
    return broken


def cmd_verify_html(html_dir: Path, base_html: Path | None) -> int:
    heading_ids = load_heading_ids()
    errors = 0
    for path, entries in heading_ids.items():
        page = html_dir / (Path(path).stem + ".html")
        if not page.exists():
            print(f"ERROR {path}: Seite {page.name} fehlt im Build")
            errors += 1
            continue
        ids = page_ids(page)
        for e in entries:
            if e["id"] not in ids:
                print(f"ERROR {page.name}: ID #{e['id']} fehlt ({e['text']})")
                errors += 1
    broken = broken_anchors(html_dir)
    if base_html is not None:
        broken -= broken_anchors(base_html)
    for page, href in sorted(broken):
        print(f"ERROR {page}: Sprungziel {href} existiert nicht")
        errors += 1
    print(f"{errors} Fehler; {sum(map(len, heading_ids.values()))} Überschriften-IDs geprüft")
    return 1 if errors else 0


def main(argv: list[str]) -> int:
    commands = {"check", "review", "english", "gen-heading-ids", "verify-html", "restore-ws"}
    command = "check"
    if argv and argv[0] in commands:
        command = argv.pop(0)
    base = BASE_COMMIT
    comments = "keep"
    html_dir = base_html = None
    all_files = False
    files: list[str] = []
    it = iter(argv)
    for a in it:
        if a == "--base":
            base = next(it)
        elif a == "--comments":
            comments = next(it)
            if comments not in ("keep", "translate-inline"):
                sys.exit("--comments: keep oder translate-inline")
        elif a == "--html":
            html_dir = Path(next(it))
        elif a == "--base-html":
            base_html = Path(next(it))
        elif a == "--all":
            all_files = True
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            files.append(a)

    if command == "gen-heading-ids":
        if html_dir is None:
            sys.exit("gen-heading-ids braucht --html DIR")
        return cmd_gen_heading_ids(html_dir, base)
    if command == "verify-html":
        if html_dir is None:
            sys.exit("verify-html braucht --html DIR")
        return cmd_verify_html(html_dir, base_html)

    selected = select_files(files, base, all_files)
    if command == "restore-ws":
        return cmd_restore_ws(selected, base)
    if command in ("review", "english"):
        return cmd_grep(command, selected, base)

    report = Report()
    cmd_check(selected, base, comments, report)
    for line in report.errors + report.warnings:
        print(line)
    print(
        f"{len(selected)} Dateien geprüft: {len(report.errors)} Fehler, "
        f"{len(report.warnings)} Warnungen"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
