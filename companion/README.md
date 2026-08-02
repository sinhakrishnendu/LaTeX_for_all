# LaTeX for All — companion examples

This directory is the runnable companion component of the single
`sinhakrishnendu/LaTeX_for_all` repository. The book is self-contained; these
files simply save readers from retyping the complete examples.

## Start here

1. Open `examples/01_first_document/main.tex`.
2. Run `latexmk -pdf main.tex` in that directory.
3. Continue through the numbered folders as needed.

Each example is independent except `07_long_project`, which demonstrates a
deliberately split project. The examples use project-relative paths and create
their build output locally.

## Build everything

From this directory:

```sh
make
```

Alternatively, run `make companion` from the repository root. The build script
compiles every `main.tex` and stops at the first error. Generated PDFs and
auxiliary files are ignored by Git.

## Folder map

- `01_first_document`: smallest working source and build command
- `02_text_structure`: headings, lists, emphasis, and reusable commands
- `03_math_units`: equations, alignment, matrices, and `siunitx`
- `04_tables`: publication-style tables with `booktabs` and `tabularx`
- `05_figures`: a self-contained TikZ workflow figure
- `06_references`: cross-references plus a Biber bibliography
- `07_long_project`: a multi-file book project
- `08_document_recipes`: article, thesis, and report starters
- `09_debugging`: a minimal diagnostic file
- `10_finish`: PDF metadata and final-build checks

## Licence

Code in this directory is available under the MIT License in `LICENSE`. The
repository's mixed licensing terms are documented in the root `LICENSE.md`.
