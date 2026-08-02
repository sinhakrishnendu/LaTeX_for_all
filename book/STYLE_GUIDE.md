# Editorial and source style guide

## Reader and voice

- Assume no knowledge of markup, programming, typesetting, or publishing.
- Use clear British English and define technical terms at first use.
- Use "we" for guided work and "you" for a direct classroom instruction.
- Explain the scholarly problem before introducing a command.
- Treat errors as evidence to inspect, not as failure.
- Prefer concrete verbs, short paragraphs, and accurate qualifications.

## Pedagogical sequence

Each completed chapter normally contains: a friendly opening; four to seven
learning outcomes; a plain-language concept explanation; a smallest working
example; source anatomy; expected output; active practice; a prediction; a
realistic error and repair; a cross-disciplinary application; good practice;
a cumulative project; summary; checklist; and exercises. New commands must be
explained where they first appear.

The continuing article grows only with concepts already taught. Examples
labelled "broken" must not use the `.tex` extension if the test runner could
mistake them for complete programs.

## LaTeX source

- UTF-8 files, two-space indentation inside environments, and readable lines.
- Straight ASCII quotation marks inside every code listing.
- Semantic commands (`\section`, `\emph`, `\caption`, `\label`) rather than
  visual improvisation.
- Label prefixes: `chap:`, `sec:`, `fig:`, `tab:`, `eq:`, and `ex:`.
- Package names use `\pkg{}`, files use `\file{}`, commands use `\cmd{}`, and
  literal source fragments use `\code{}` in prose.
- Avoid `\bf`, `\it`, `\centerline`, `$$`, `eqnarray`, `epsfig`, and the
  obsolete `subfigure` package.
- Do not hard-code figure, table, equation, section, or page numbers.
- Keep machine-specific paths out of source and examples.

## Visual system

- Trim: 7 by 10 inches with a comfortable inner margin.
- Body and code: Latin Modern families distributed with TeX Live.
- Interior colour: black only, with a robust 12 percent black title tint.
  Meaning must never depend on colour or a light screen surviving production.
- Boxes: short, breakable, square-cornered, strongly ruled, and subordinate to
  the main prose. Avoid reversed type and large solid ink areas.
- Figures: use black marks, direct labels, and line styles at or above 0.65 pt;
  retain legibility on absorbent uncoated or groundwood paper.
- Cover: a separate full-colour production file; the monochrome interior
  profile does not alter it.
- Tables: `booktabs` rules, no vertical lines by default.
- Captions: informative, left aligned, and understandable with the figure or
  table.

## References and assets

Only add a bibliographic record after checking an authoritative source. Do
not infer DOIs, editions, dates, or URLs. Record licences and provenance for
non-original assets in `assets/ASSET_REQUESTS.md`. Original diagrams should
keep editable source beside the exported figure.
