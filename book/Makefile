LATEXMK ?= latexmk
BOOK_PDF := output/pdf/latex_for_all.pdf

.PHONY: all book cover examples templates code-audit check clean

all: book cover examples templates code-audit check

book:
	mkdir -p output/pdf build
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex
	cp -f build/main.pdf $(BOOK_PDF)

cover:
	mkdir -p output/pdf build/cover
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error \
		-outdir=build/cover cover/full_cover.tex
	cp -f build/cover/full_cover.pdf output/pdf/latex_for_all_full_cover.pdf

examples:
	./scripts/compile_all_examples.sh

templates:
	./scripts/compile_templates.sh

code-audit:
	python3 ./scripts/audit_book_code.py

check:
	./scripts/check_project.sh

clean:
	$(LATEXMK) -C main.tex
