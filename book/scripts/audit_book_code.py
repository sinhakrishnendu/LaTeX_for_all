#!/usr/bin/env python3
"""Audit the code printed in the book.

Complete LaTeX documents are extracted and compiled in isolated directories.
BibLaTeX records are processed with Biber. Contextual fragments are checked for
balanced groups and environments, and actionable terminal listings are parsed
by the POSIX shell without being executed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "code_audit"
REPORT = BUILD / "report.tsv"
LATEX_BEGIN = r"\begin{latexcode}{"
LATEX_END = r"\end{latexcode}"
TERMINAL_BEGIN = r"\begin{terminalcode}{"
TERMINAL_END = r"\end{terminalcode}"


@dataclass(frozen=True)
class Listing:
    kind: str
    source: Path
    line: int
    title: str
    body: str


def extract_listings() -> list[Listing]:
    listings: list[Listing] = []
    # Audit every source area included by the full book driver, including the
    # complete practical coding section added after each chapter.
    for folder in ("frontmatter", "chapters", "practical", "backmatter"):
        for source in sorted((ROOT / folder).glob("*.tex")):
            lines = source.read_text(encoding="utf-8").splitlines()
            active_kind: str | None = None
            title = ""
            start = 0
            body: list[str] = []
            for number, line in enumerate(lines, start=1):
                if active_kind is None:
                    if line.startswith(LATEX_BEGIN) and line.endswith("}"):
                        active_kind = "latex"
                        title = line[len(LATEX_BEGIN) : -1]
                        start = number
                        body = []
                    elif line.startswith(TERMINAL_BEGIN) and line.endswith("}"):
                        active_kind = "terminal"
                        title = line[len(TERMINAL_BEGIN) : -1]
                        start = number
                        body = []
                    continue

                closing = LATEX_END if active_kind == "latex" else TERMINAL_END
                if line == closing:
                    listings.append(
                        Listing(
                            active_kind,
                            source.relative_to(ROOT),
                            start,
                            title,
                            "\n".join(body).rstrip() + "\n",
                        )
                    )
                    active_kind = None
                    title = ""
                    body = []
                else:
                    body.append(line)

            if active_kind is not None:
                raise RuntimeError(f"Unclosed {active_kind} listing in {source}:{start}")
    return listings


def diagnostic_listing(title: str) -> bool:
    lowered = title.lower()
    markers = (
        "broken",
        "incomplete",
        "non-portable",
        "case-sensitive",
        "undefined-command report",
    )
    return any(marker in lowered for marker in markers)


def explicitly_partial_listing(title: str) -> bool:
    lowered = title.lower()
    return lowered in {"corrected line", "corrected closing line"}


def strip_tex_comments_and_verbs(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        line = re.sub(r"\\verb(.).*?\1", "", line)
        position = 0
        while True:
            match = re.search(r"(?<!\\)%", line[position:])
            if match is None:
                cleaned.append(line)
                break
            cut = position + match.start()
            preceding = len(line[:cut]) - len(line[:cut].rstrip("\\"))
            if preceding % 2 == 0:
                cleaned.append(line[:cut])
                break
            position = cut + 1
    return "\n".join(cleaned)


def structural_errors(text: str) -> list[str]:
    text = strip_tex_comments_and_verbs(text)
    errors: list[str] = []
    depth = 0
    for index, char in enumerate(text):
        if char not in "{}":
            continue
        preceding = len(text[:index]) - len(text[:index].rstrip("\\"))
        if preceding % 2 == 1:
            continue
        depth += 1 if char == "{" else -1
        if depth < 0:
            errors.append("closing brace without an opening brace")
            depth = 0
    if depth:
        errors.append(f"{depth} unclosed brace group(s)")

    stack: list[str] = []
    for match in re.finditer(r"\\(begin|end)\{([^{}]+)\}", text):
        action, environment = match.groups()
        if action == "begin":
            stack.append(environment)
        elif stack and stack[-1] == environment:
            stack.pop()
        else:
            expected = stack[-1] if stack else "none"
            errors.append(
                f"environment closes as {environment!r}; expected {expected!r}"
            )
    if stack:
        errors.append("unclosed environment(s): " + ", ".join(stack))
    return errors


def safe_slug(index: int, listing: Listing) -> str:
    title = re.sub(r"[^a-z0-9]+", "-", listing.title.lower()).strip("-")
    return f"{index:03d}-{title[:55] or 'listing'}"


def write_common_fixtures(case: Path) -> None:
    for folder in (
        "figures",
        "figures/original",
        "preamble",
        "frontmatter",
        "chapters",
        "appendices",
    ):
        (case / folder).mkdir(parents=True, exist_ok=True)

    figure = ROOT / "build" / "figures" / "method_comparison.pdf"
    difference = ROOT / "build" / "figures" / "difference_plot.pdf"
    if not figure.exists() or not difference.exists():
        raise RuntimeError("Build the original figures before running the code audit")
    for target in (
        case / "method_comparison.pdf",
        case / "measurement-methods.pdf",
        case / "plot.pdf",
        case / "figures" / "sample.pdf",
        case / "figures" / "original" / "method_comparison.pdf",
    ):
        shutil.copy2(figure, target)
    shutil.copy2(difference, case / "figures" / "original" / "difference_plot.pdf")

    bibliography = (ROOT / "bibliography" / "references.bib").read_text(
        encoding="utf-8"
    )
    if "@online{latexproject," not in bibliography:
        bibliography += r"""

@online{latexproject,
  author  = {{The \LaTeX{} Project}},
  title   = {The \LaTeX{} Project},
  url     = {https://www.latex-project.org/},
  urldate = {2026-07-31}
}
"""
    (case / "references.bib").write_text(bibliography, encoding="utf-8")

    (case / "preamble" / "packages.tex").write_text(
        "\\usepackage[backend=biber,style=authoryear]{biblatex}\n"
        "\\addbibresource{references.bib}\n",
        encoding="utf-8",
    )
    (case / "preamble" / "commands.tex").write_text(
        "% Shared commands would be defined here.\n", encoding="utf-8"
    )
    stubs = {
        "frontmatter/abstract.tex": "\\chapter*{Abstract}\nA concise abstract.\n",
        "chapters/introduction.tex": "\\chapter{Introduction}\nIntroduction text.\n",
        "chapters/methods.tex": "\\chapter{Methods}\nMethods text.\n",
        "appendices/supplementary_methods.tex": (
            "\\chapter{Supplementary Methods}\nSupplementary detail.\n"
        ),
        "title-page.tex": (
            "\\begin{titlepage}\\centering{\\Large Thesis Title\\par}"
            "\\vfill Your Name\\end{titlepage}\n"
        ),
        "chapter-one.tex": "\\chapter{Introduction}\nIntroductory text.\n",
    }
    for relative, content in stubs.items():
        (case / relative).write_text(content, encoding="utf-8")


def run(command: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def compile_latex(
    index: int, listing: Listing, env: dict[str, str]
) -> tuple[str, str]:
    case = BUILD / "complete" / safe_slug(index, listing)
    case.mkdir(parents=True, exist_ok=True)
    write_common_fixtures(case)
    source = case / "snippet.tex"
    source.write_text(listing.body, encoding="utf-8")
    out = case / "out"
    out.mkdir(exist_ok=True)
    # TeX writes a separate .aux file beside each \include target.  Mirror
    # the common project subdirectories when compiling with -outdir so that
    # otherwise valid multi-file examples remain writable.
    for folder in ("frontmatter", "chapters", "appendices"):
        (out / folder).mkdir(parents=True, exist_ok=True)
    result = run(
        [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={out}",
            source.name,
        ],
        case,
        env,
    )
    (case / "console.log").write_text(result.stdout, encoding="utf-8")
    expected_failure = diagnostic_listing(listing.title)
    if expected_failure:
        if result.returncode == 0:
            return "FAIL", "intentional broken example compiled unexpectedly"
        return "PASS_EXPECTED_FAILURE", "failed as the teaching example states"

    if result.returncode != 0:
        tail = " | ".join(result.stdout.splitlines()[-5:])
        return "FAIL", f"complete document did not compile: {tail}"
    log = out / "snippet.log"
    if log.exists():
        warnings = re.findall(
            r"(undefined citations|undefined references|multiply defined)",
            log.read_text(encoding="utf-8", errors="replace"),
            flags=re.IGNORECASE,
        )
        if warnings:
            return "FAIL", "unresolved build warning: " + ", ".join(sorted(set(warnings)))
    return "PASS_COMPILED", "complete document compiled"


def compile_bibliography(
    index: int, listing: Listing, env: dict[str, str]
) -> tuple[str, str]:
    case = BUILD / "bibliography" / safe_slug(index, listing)
    case.mkdir(parents=True, exist_ok=True)
    (case / "references.bib").write_text(listing.body, encoding="utf-8")
    (case / "main.tex").write_text(
        "\\documentclass{article}\n"
        "\\usepackage[backend=biber,style=authoryear]{biblatex}\n"
        "\\addbibresource{references.bib}\n"
        "\\begin{document}\\nocite{*}\\printbibliography\\end{document}\n",
        encoding="utf-8",
    )
    out = case / "out"
    out.mkdir(exist_ok=True)
    result = run(
        [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={out}",
            "main.tex",
        ],
        case,
        env,
    )
    (case / "console.log").write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        tail = " | ".join(result.stdout.splitlines()[-5:])
        return "FAIL", f"bibliography record did not process: {tail}"
    return "PASS_BIBER", "bibliography record processed with Biber"


def terminal_is_actionable(title: str, body: str) -> bool:
    lowered = title.lower()
    displays = ("tree", "map", "report")
    tree_art = re.search(r"(?m)^\s*\|--", body) is not None
    return not any(marker in lowered for marker in displays) and not tree_art


def main() -> int:
    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir(parents=True)
    env = os.environ.copy()
    # Respect an explicitly selected TeX tree for reproducible release builds.
    # Otherwise retain the project's intentionally isolated default.
    env.setdefault("TEXMFHOME", str(ROOT / ".texmfhome"))
    # Keep generated formats and bitmap-font caches inside the disposable
    # audit tree rather than relying on a user-level TeX cache being writable.
    env["TEXMFVAR"] = str(BUILD / "texmf-var")
    env["TEXMFCONFIG"] = str(BUILD / "texmf-config")
    Path(env["TEXMFVAR"]).mkdir(parents=True, exist_ok=True)
    Path(env["TEXMFCONFIG"]).mkdir(parents=True, exist_ok=True)
    listings = extract_listings()
    rows: list[tuple[str, str, int, str, str, str]] = []
    failures = 0

    for index, listing in enumerate(listings, start=1):
        status = "PASS"
        note = ""
        if listing.kind == "latex":
            complete = all(
                token in listing.body
                for token in (
                    r"\documentclass",
                    r"\begin{document}",
                    r"\end{document}",
                )
            )
            bibliography = listing.body.lstrip().startswith("@")
            if complete:
                status, note = compile_latex(index, listing, env)
            elif bibliography:
                status, note = compile_bibliography(index, listing, env)
            else:
                errors = structural_errors(listing.body)
                if errors and explicitly_partial_listing(listing.title):
                    status = "PASS_CONTEXT_FRAGMENT"
                    note = "explicitly partial corrected line"
                elif errors and not diagnostic_listing(listing.title):
                    status = "FAIL"
                    note = "; ".join(errors)
                elif errors:
                    status = "PASS_EXPECTED_DIAGNOSTIC"
                    note = "; ".join(errors)
                else:
                    status = "PASS_CONTEXT_FRAGMENT"
                    note = "balanced contextual fragment"
        elif terminal_is_actionable(listing.title, listing.body):
            result = subprocess.run(
                ["/bin/sh", "-n"],
                input=listing.body,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            if result.returncode:
                status = "FAIL"
                note = "shell syntax: " + result.stdout.strip()
            else:
                status = "PASS_SHELL_SYNTAX"
                note = "POSIX shell syntax parsed; command not executed"
        else:
            status = "PASS_DISPLAY"
            note = "terminal output/tree display; not an executable listing"

        if status == "FAIL":
            failures += 1
        rows.append(
            (
                status,
                str(listing.source),
                listing.line,
                listing.kind,
                listing.title,
                note,
            )
        )

    with REPORT.open("w", encoding="utf-8") as handle:
        handle.write("status\tsource\tline\tkind\ttitle\tnote\n")
        for row in rows:
            handle.write("\t".join(str(item).replace("\t", " ") for item in row) + "\n")

    counts: dict[str, int] = {}
    for row in rows:
        counts[row[0]] = counts.get(row[0], 0) + 1
    print(f"Audited {len(rows)} printed code listings; {failures} failed.")
    for status in sorted(counts):
        print(f"{status}: {counts[status]}")
    print(f"Results: {REPORT}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
