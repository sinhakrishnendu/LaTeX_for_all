# Full cover notes

`full_cover.tex` produces a one-page wraparound cover in this order:

`back cover | spine | front cover`

The current production assumptions are:

- trim size: 7 × 10 inches;
- bleed: 0.125 inch on every outer edge;
- full practical-edition page count: 264 pages, including a blank final verso;
- calculated spine: 0.620 inch;
- total artwork: 14.870 × 10.250 inches.

The photograph on the front is the enhanced portrait derivative stored at
`figures/cover/mountain_road_enhanced_300dpi.png`. At its placed width it
provides approximately 300 pixels per inch.

The current width is proportional to the 0.552 inch spine and 14.802 inch
total width that KDP reported for the former 235-page edition. At 264 pages,
the resulting spine rounds to 0.620 inch and the wrap to 14.870 inches. If KDP
reports a different expected width after the interior is uploaded, use that
calculator value. No barcode box is drawn because Amazon will place its
barcode automatically during cover processing.

Build from the project root with:

```sh
latexmk -pdf -outdir=build/cover cover/full_cover.tex
```

## KDP artificial-intelligence declaration

The front-cover photograph was extended and refined with an image-generation
tool. Under the KDP Content Guidelines current on 2026-08-01, this should be
declared to KDP as AI-generated cover content during publication. The separate
editorial revision and code checking described in the acknowledgements are
AI-assisted uses. Recheck the current KDP form and guidance before every new
edition:

https://kdp.amazon.com/en_US/help/topic/G200672390
