.PHONY: all book cover companion doctor verify release clean

all: book cover companion

book:
	$(MAKE) -C book book

cover:
	$(MAKE) -C book cover

companion:
	$(MAKE) -C companion

doctor:
	@missing=0; \
	for tool in latexmk biber python3 gs rg; do \
		if ! command -v $$tool >/dev/null 2>&1; then \
			echo "Missing required tool: $$tool"; \
			missing=1; \
		fi; \
	done; \
	test $$missing -eq 0

verify: doctor book
	$(MAKE) -C book code-audit
	$(MAKE) -C book check

release: doctor
	$(MAKE) -C book book cover examples templates code-audit check
	$(MAKE) -C companion

clean:
	$(MAKE) -C book clean
	$(MAKE) -C companion clean
