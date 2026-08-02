#!/usr/bin/env sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
build_root="$project_root/build/examples"
results_file="$build_root/results.tsv"
TEXMFHOME="$project_root/.texmfhome"
export TEXMFHOME

mkdir -p "$build_root" "$TEXMFHOME"
: > "$results_file"

failures=0
count=0

{
  find "$project_root/examples" -type f -name '*.tex' -print
  find "$project_root/running_project" -type f -name 'main.tex' -print
} | sort | while IFS= read -r source; do
  count=$((count + 1))
  relative=${source#"$project_root/"}
  safe_name=$(printf '%s' "$relative" | tr '/ ' '__')
  example_build="$build_root/$safe_name"
  source_dir=$(dirname "$source")
  source_name=$(basename "$source")
  mkdir -p "$example_build"

  if (cd "$source_dir" && latexmk -pdf -interaction=nonstopmode \
      -halt-on-error -outdir="$example_build" "$source_name") \
      > "$example_build/console.log" 2>&1; then
    printf 'PASS\t%s\n' "$relative" >> "$results_file"
  else
    printf 'FAIL\t%s\n' "$relative" >> "$results_file"
    failures=$((failures + 1))
  fi

  printf '%s\n' "$count $failures" > "$build_root/counts.tmp"
done

if [ -f "$build_root/counts.tmp" ]; then
  set -- $(sed -n '1p' "$build_root/counts.tmp")
  count=$1
  failures=$2
fi

printf 'Compiled %s standalone examples; %s failed.\n' "$count" "$failures"
printf 'Results: %s\n' "$results_file"

[ "$failures" -eq 0 ]
