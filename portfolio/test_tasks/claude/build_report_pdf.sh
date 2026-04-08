#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HTML_FILE="$ROOT_DIR/kurganskii_anton_test_task_ai_operator.html"
PDF_FILE="$ROOT_DIR/kurganskii_anton_test_task_ai_operator.pdf"

"$ROOT_DIR/build_report_html.sh"

playwright pdf \
  --browser chromium \
  --paper-format A4 \
  --wait-for-timeout 7000 \
  "file://$HTML_FILE" \
  "$PDF_FILE"

echo "PDF built: $PDF_FILE"
