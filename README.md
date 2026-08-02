# LaTeX for All

[![Quality checks](https://github.com/sinhakrishnendu/LaTeX_for_all/actions/workflows/quality.yml/badge.svg)](https://github.com/sinhakrishnendu/LaTeX_for_all/actions/workflows/quality.yml)
[![Book licence: CC BY 4.0](https://img.shields.io/badge/book%20licence-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code licence: MIT](https://img.shields.io/badge/code%20licence-MIT-blue.svg)](LICENSE.md)

Production source, publication assets, and reader companion material for
*LaTeX for All: From Your First Document to Publication-Ready Scholarly
Writing* by Krishnendu Sinha.

This is the single canonical repository for the book. The printed book is
self-contained; the companion files are optional, runnable versions of useful
examples.

## Repository structure

| Path | Contents |
|---|---|
| `book/` | Complete 22-chapter manuscript, practical sections, cover source, figures, templates, and release checks |
| `companion/` | Reader-ready examples, document starters, checklists, and build scripts |
| `assets/reference/` | Author-supplied visual references retained for publication provenance |
| `.github/` | Continuous-integration workflow and contribution templates |

## Current print specification

- Title: *LaTeX for All*
- ISBN: `9798190207026`
- Interior: 264 pages, 7 × 10 inches, black-only
- Cover: 14.870 × 10.250 inches, full colour, 0.620-inch derived spine
- Publishing route: independently published through Amazon KDP

KDP's cover calculator value takes precedence if it reports a different
expected width after processing the uploaded interior.

## Build requirements

- A current TeX Live or MiKTeX installation
- `latexmk` and Biber
- Python 3
- Ghostscript and ripgrep for release checks

## Quick start

From the repository root:

```sh
make doctor     # confirm release tools are available on PATH
make book       # build the print interior
make cover      # build the full-colour wrap
make companion  # compile all reader examples
make verify     # audit printed code and production constraints
```

For a complete release build:

```sh
make release
```

Generated PDFs are written below `book/output/pdf/`. They are intentionally
excluded from Git history; attach approved binaries to a GitHub Release.

## Quality controls

The release workflow checks complete LaTeX examples, BibLaTeX/Biber records,
contextual code fragments, shell syntax, duplicate labels, unresolved
references, inclusive language, and black-only interior separations. The
current edition contains 172 audited printed listings.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for editorial, code, and build
requirements. Contributions should preserve the self-contained character of
the book and must not introduce unverified scientific claims or private data.

## Citation

Repository citation metadata are provided in [CITATION.cff](CITATION.cff).
The preferred book citation is:

> Sinha, Krishnendu. *LaTeX for All: From Your First Document to
> Publication-Ready Scholarly Writing*. Independently published, 2026.
> ISBN 9798190207026.

## Licensing

Original book text, LaTeX source, diagrams, and teaching data are available
under CC BY 4.0. Code examples are additionally available under the MIT
License. Cover artwork, visual references, trademarks, and third-party
material are excluded unless explicitly stated otherwise. See
[LICENSE.md](LICENSE.md) for the complete terms.
