#!/usr/bin/env sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
build_root="$project_root/build/templates"
TEXMFHOME="$project_root/.texmfhome"
export TEXMFHOME
mkdir -p "$build_root" "$TEXMFHOME"

failures=0
found=0

for template in scholarly_article thesis technical_report; do
  source_dir="$project_root/templates/$template"
  if [ ! -f "$source_dir/main.tex" ]; then
    printf 'FAIL %s (missing main.tex)\n' "$template"
    failures=$((failures + 1))
    continue
  fi

  found=$((found + 1))
  output_dir="$build_root/$template"
  mkdir -p "$output_dir" "$output_dir/chapters" "$output_dir/appendices"
  if (cd "$source_dir" && latexmk -pdf -interaction=nonstopmode \
      -halt-on-error -outdir="$output_dir" main.tex) \
      > "$output_dir/console.log" 2>&1; then
    printf 'PASS %s\n' "$template"
  else
    printf 'FAIL %s\n' "$template"
    failures=$((failures + 1))
  fi
done

printf 'Compiled %s available templates; %s failed.\n' "$found" "$failures"
[ "$failures" -eq 0 ]
