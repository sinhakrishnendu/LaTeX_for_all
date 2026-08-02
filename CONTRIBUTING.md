# Contributing

Thank you for helping improve *LaTeX for All*. Contributions may address the
book source, runnable companion examples, build tooling, or verified
publication-quality corrections.

## Before making a change

1. Search existing issues and pull requests for related work.
2. Keep each change focused and explain the reader or production problem it
   solves.
3. Do not add confidential information, unpublished research data, or claims
   that cannot be checked from an authoritative source.

## Editorial conventions

- Use British English in the manuscript.
- Use `\LaTeX{}` for the typeset product name in prose.
- Prefer semantic LaTeX commands to manual visual formatting.
- Keep examples self-contained, portable, and reproducible.
- Label simulated teaching data explicitly.
- Preserve a black-only interior; the cover is maintained separately in
  colour.
- Use project-relative paths only.

## Build and test

Run the relevant focused build, followed by the complete verification target:

```sh
make book
make companion
make verify
```

For release-affecting changes, run:

```sh
make release
```

Inspect changed PDF pages visually. Changes affecting pagination must also be
checked against the KDP cover calculator before release.

## Pull requests

Describe the motivation, list the files or chapters affected, and include the
commands used for verification. Do not commit generated build directories,
auxiliary files, or release PDFs.
