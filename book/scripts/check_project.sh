#!/usr/bin/env sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_root"

failures=0

check_for_pattern() {
  label=$1
  pattern=$2
  shift 2
  if rg -n "$pattern" "$@" > "build/check_${label}.log" 2>/dev/null; then
    printf 'FAIL %-24s see build/check_%s.log\n' "$label" "$label"
    failures=$((failures + 1))
  else
    printf 'PASS %s\n' "$label"
  fi
}

mkdir -p build

check_for_pattern smart_quotes '[“”‘’]' \
  --glob '*.tex' --glob '!build/**' .
check_for_pattern obsolete_font_commands '\\(bf|it)([^A-Za-z]|$)' \
  --glob '*.tex' --glob '!build/**' .
check_for_pattern obsolete_display_math '\$\$' \
  --glob '*.tex' --glob '!build/**' \
  --glob '!chapters/chapter06_mathematics_beginning.tex' .
check_for_pattern obsolete_eqnarray 'eqnarray' \
  --glob '*.tex' --glob '!build/**' \
  --glob '!chapters/chapter06_mathematics_beginning.tex' \
  --glob '!backmatter/solutions.tex' .
check_for_pattern obsolete_graphics '(epsfig|usepackage(\[[^]]*\])?\{subfigure\})' \
  --glob '*.tex' --glob '!build/**' .
check_for_pattern absolute_source_paths '(/Users/|[A-Za-z]:\\\\)' \
  --glob '*.tex' --glob '!build/**' \
  --glob '!chapters/chapter18_collaboration.tex' .
check_for_pattern exclusionary_language \
  '\b(blacklist|whitelist|slave|master|grandfathered|crazy|insane|idiot|stupid|dumb|crippled?|oriental|primitive|blinded|blind review)\b' \
  --glob '*.tex' --glob '*.md' --glob '*.bib' --glob '*.R' \
  --glob '!build/**' --glob '!tmp/**' --glob '!output/**' .

check_duplicate_group() {
  group=$1
  shift
  labels_file="build/check_labels_${group}.txt"
  duplicates_file="build/check_duplicate_labels_${group}.log"
  rg -o --no-filename '\\label\{[^}]+\}' --glob '*.tex' "$@" \
    | sort > "$labels_file" || true
  uniq -d "$labels_file" > "$duplicates_file"
  if [ -s "$duplicates_file" ]; then
    printf 'FAIL duplicate_labels_%-12s see %s\n' "$group" "$duplicates_file"
    failures=$((failures + 1))
  else
    printf 'PASS duplicate_labels_%s\n' "$group"
  fi
}

check_duplicate_group book main.tex metadata.tex preamble frontmatter chapters backmatter
check_duplicate_group running_project running_project/measurement_methods_article
check_duplicate_group article_template templates/scholarly_article
check_duplicate_group thesis_template templates/thesis
check_duplicate_group report_template templates/technical_report

if [ -f build/main.log ]; then
  if rg -n 'undefined citations|undefined references|multiply defined' \
      build/main.log > build/check_build_warnings.log; then
    printf 'FAIL build_reference_warnings see build/check_build_warnings.log\n'
    failures=$((failures + 1))
  else
    printf 'PASS build_reference_warnings\n'
  fi
fi

if [ -f output/pdf/latex_for_all.pdf ] && command -v gs >/dev/null 2>&1; then
  if gs -q -o - -sDEVICE=inkcov output/pdf/latex_for_all.pdf \
      | awk '
          NF >= 4 {
            cyan += $1
            magenta += $2
            yellow += $3
          }
          END {
            printf "C=%.6f M=%.6f Y=%.6f\n", cyan, magenta, yellow
            if (cyan > 0.00001 || magenta > 0.00001 || yellow > 0.00001) {
              exit 1
            }
          }' > build/check_monochrome_pdf.log; then
    printf 'PASS monochrome_press_pdf\n'
  else
    printf 'FAIL %-24s see build/check_monochrome_pdf.log\n' monochrome_press_pdf
    failures=$((failures + 1))
  fi
fi

printf 'Quality checks complete; %s failed.\n' "$failures"
[ "$failures" -eq 0 ]
