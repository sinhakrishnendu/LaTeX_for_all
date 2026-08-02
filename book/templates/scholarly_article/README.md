# Scholarly article template

This independent template demonstrates a generic, publisher-neutral research
article. Its data and results are simulated for teaching.

Build from this directory with:

```sh
latexmk -pdf main.tex
```

Edit the metadata block in `main.tex`, replace every `[PLACEHOLDER]`, and adapt
the declarations to the target journal. Consult the journal's current author
instructions before replacing `article` with a publisher class. To prepare an
anonymous draft, set `\anonymoustrue`; remove identifying acknowledgements and
self-identifying repository links as well.

Key files:

- `main.tex`: class, packages, metadata, and section order;
- `sections/`: manuscript prose;
- `references.bib`: bibliography database;
- `figures/method_comparison.pdf`: original, editable source is in
  `../../figures/original/method_comparison.tex`.

Clean generated files with `latexmk -C`.
