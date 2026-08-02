# Measurement-methods running project

This educational article grows through the book and is now a complete
multi-file manuscript. All values and findings are simulated demonstrations;
they do not describe a real experiment, survey, patient group, clinical study,
or validated instrument.

Build the article from this directory with `latexmk -pdf main.tex`. Verify its
three rounded results, if R is installed, with `Rscript analysis/check_results.R`.
Set `\anonymoustrue` in `preamble.tex` for the visible anonymous variant, then
audit all metadata and files as described in Chapter 16.

Project map:

- `main.tex`: official entry point and section order;
- `preamble.tex`: packages, bibliography, and anonymity toggle;
- `sections/`: manuscript content and declarations;
- `data/`: simulated CSV and data note;
- `analysis/`: portable numerical verification;
- `figures/`: derived original teaching figures;
- `references.bib`: verified bibliography records.
- `SUBMISSION_CHECKLIST.md`: a venue-neutral practice release audit.

Replace every placeholder and consult current venue instructions before any
real submission.
