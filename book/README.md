# LaTeX for All — production source

Production source for *LaTeX for All: From Your First Document to
Publication-Ready Scholarly Writing* by Krishnendu Sinha.

The current full practical edition retains all 22 original chapters. Every
chapter is followed by a separate **Complete Practical Coding** section with a
full runnable file and a short modification task. An early scope statement
identifies the advanced subjects intentionally outside the primary coverage.

## Build requirements

- A current TeX Live or MiKTeX distribution
- `latexmk` and Biber
- Poppler and Ghostscript for release checks

The source uses UTF-8 and pdfLaTeX. It requires no commercial fonts.

## Build the book and cover

From this directory:

```sh
make book
make cover
```

From the repository root, the equivalent commands are also `make book` and
`make cover`.

Outputs:

- `output/pdf/latex_for_all.pdf`
- `output/pdf/latex_for_all_full_cover.pdf`

The 264-page interior uses a 7 × 10 inch trim and ends with a deliberate blank
verso. The current full-colour wrap is 14.870 × 10.250 inches, including outer
bleed and the derived 0.620-inch spine. KDP's calculator value takes precedence
if it reports a different expected width after upload.

## Page-opening policy

Part-title pages always begin on recto pages. Chapters use the next available
page, a deliberate economical-paperback choice that avoids a blank leaf before
every chapter. Practical sections flow directly after their related chapters.

## Print profile

The interior is black-only and suitable for economical printing on absorbent
uncoated or groundwood paper. The cover remains a separate colour PDF. No
barcode box is drawn because Amazon adds the barcode automatically.

## Test the release

```sh
make code-audit
scripts/check_project.sh
```

The printed-code audit extracts complete documents, bibliography records,
contextual fragments, and terminal commands from all included chapter,
practical, front-matter, and back-matter sources. Complete documents are
compiled in isolation.

Standalone examples and reusable templates can also be checked with:

```sh
scripts/compile_all_examples.sh
make templates
```

## Companion material

The canonical repository is `sinhakrishnendu/LaTeX_for_all`. Its
`companion/` directory contains runnable example files, a multi-file project,
document starters, checklists, and build scripts. The printed book remains
self-contained and does not require those optional files.

## Main source locations

- Book driver and order: `main.tex`
- Identity and ISBN: `metadata.tex`
- Original chapters: `chapters/`
- Complete chapter-by-chapter coding sections: `practical/`
- Early scope statement: `frontmatter/scope.tex`
- Shared packages and design: `preamble/`
- Back matter: `backmatter/`
- Full-colour cover: `cover/`
- Automated tests: `scripts/`
- Generated PDFs: `output/pdf/`

Except where otherwise noted, original book material is available under CC BY
4.0 and code examples are also available under the MIT License. Cover artwork
is excluded unless separately licensed; see `LICENSE.md` for the complete
terms.
