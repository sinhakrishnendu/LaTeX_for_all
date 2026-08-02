# Release checklist

## Source and verification

- [ ] `make release` completes without errors.
- [ ] Printed-code audit reports zero failures.
- [ ] References, citations, index, and bookmarks resolve.
- [ ] Changed tables and figures have been inspected at print size.
- [ ] Interior colour-separation check reports zero cyan, magenta, and yellow.
- [ ] Fonts are embedded and the trim size is 7 × 10 inches.
- [ ] Final page count is even and the last verso is blank.

## KDP files

- [ ] Interior PDF is copied from `book/output/pdf/latex_for_all.pdf`.
- [ ] KDP's current spine calculation matches the cover source.
- [ ] Full wrap dimensions match KDP's value exactly.
- [ ] Cover remains full colour and contains no reserved barcode box.
- [ ] ISBN and dedication appear only where intended in the interior.
- [ ] AI-generated cover content and AI-assisted editorial work are declared
      accurately in the current KDP submission form.

## Repository release

- [ ] Working tree is clean and the release commit is on `main`.
- [ ] `CITATION.cff`, README specifications, and changelog are current.
- [ ] Approved interior and cover PDFs are attached to the GitHub Release.
- [ ] Release tag follows `vMAJOR.MINOR.PATCH`.
