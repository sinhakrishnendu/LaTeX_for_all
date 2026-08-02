#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

find "$repo_root/examples" -name main.tex -print | sort |
while IFS= read -r main_file; do
  example_dir=$(dirname "$main_file")
  printf 'Compiling %s\n' "${example_dir#"$repo_root/"}"
  (
    cd "$example_dir"
    mkdir -p build
    latexmk -pdf -interaction=nonstopmode -halt-on-error \
      -outdir=build main.tex
  )
done

printf 'All companion examples compiled successfully.\n'
