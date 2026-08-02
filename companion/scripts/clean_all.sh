#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

find "$repo_root/examples" -name main.tex -print | sort |
while IFS= read -r main_file; do
  example_dir=$(dirname "$main_file")
  (
    cd "$example_dir"
    latexmk -C -outdir=build main.tex >/dev/null
  )
done

printf 'Generated example files cleaned.\n'
