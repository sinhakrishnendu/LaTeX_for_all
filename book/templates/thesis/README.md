# Generic thesis template

This is an independent, publisher-neutral thesis project. It demonstrates a
multi-file structure, Roman-numbered front matter, Arabic-numbered chapters,
lists, abbreviations, bibliography, and appendices.

Build from this directory with:

```sh
latexmk -pdf main.tex
```

Before use, obtain the current regulations and official class or template from
your institution. Then replace every `[PLACEHOLDER]`. The certificate,
declaration, signature, deposit, accessibility, paper-size, and embargo
requirements are intentionally generic and must be verified locally. Do not
invent approvals or signatures.

`metadata.tex` centralises names and title. Content is under `frontmatter/`,
`chapters/`, and `appendices/`; `references.bib` is the bibliography database.
The sample results are simulated.
