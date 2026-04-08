#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_FILE="$ROOT_DIR/kurganskii_anton_test_task_ai_operator.md"
OUTPUT_FILE="$ROOT_DIR/kurganskii_anton_test_task_ai_operator.html"
TEMPLATE_FILE="$ROOT_DIR/report.template.html"
CSS_FILE="$ROOT_DIR/report.css"
MERMAID_FILE="$ROOT_DIR/mermaid-init.html"

pandoc "$INPUT_FILE" \
  --from gfm \
  --to html5 \
  --standalone \
  --section-divs \
  --template "$TEMPLATE_FILE" \
  --css "$(basename "$CSS_FILE")" \
  --include-after-body "$MERMAID_FILE" \
  --metadata lang=ru \
  --metadata title="Аналитический документ: Логика AI-оператора" \
  -o "$OUTPUT_FILE"

echo "HTML built: $OUTPUT_FILE"
