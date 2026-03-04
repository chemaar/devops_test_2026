#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="$ROOT_DIR/docs"
BUILD_DIR="$ROOT_DIR/site"
TMP_MD="$BUILD_DIR/pandoc_input.md"
OUTPUT_PDF="$BUILD_DIR/Podcastify_doc.pdf"

mkdir -p "$BUILD_DIR"

ROOT_DIR="$ROOT_DIR" python3 - <<'PY'
from pathlib import Path
import os
import re

root = Path(os.environ["ROOT_DIR"])
docs = root / "docs"
out = root / "site" / "pandoc_input.md"

source_files = [docs / "index.md", docs / "spec.md", docs / "architecture.md"]
include_re = re.compile(r'^\s*--8<--\s+"([^"]+)"\s*$')

parts: list[str] = []

for i, file_path in enumerate(source_files):
    content_lines: list[str] = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        match = include_re.match(line)
        if match:
            include_path = root / match.group(1)
            if include_path.exists() and include_path.is_file():
                content_lines.append(include_path.read_text(encoding="utf-8").rstrip("\n"))
            else:
                raise FileNotFoundError(f"No se encontró el include: {match.group(1)}")
        else:
            content_lines.append(line)

    parts.append("\n".join(content_lines).strip())
    if i < len(source_files) - 1:
        parts.append("\\newpage")

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n\n".join(parts).strip() + "\n", encoding="utf-8")
PY

run_local_pandoc() {
  pandoc "$TMP_MD" \
    --from markdown \
    --toc \
    --metadata title="Proyecto Podcastify" \
    -o "$OUTPUT_PDF"
}

run_docker_pandoc() {
  docker run --rm \
    -v "$ROOT_DIR:/data" \
    pandoc/latex:latest \
    "/data/site/pandoc_input.md" \
    --from markdown \
    --toc \
    --metadata title="Proyecto Podcastify" \
    -o "/data/site/Podcastify_doc.pdf"
}

if command -v pandoc >/dev/null 2>&1; then
  echo "[info] Usando pandoc local"
  if run_local_pandoc; then
    echo "[ok] PDF generado en: $OUTPUT_PDF"
    exit 0
  fi
  echo "[warn] Falló pandoc local; intentando con Docker..."
fi

if command -v docker >/dev/null 2>&1; then
  echo "[info] Usando pandoc/latex en Docker"
  run_docker_pandoc
  echo "[ok] PDF generado en: $OUTPUT_PDF"
  exit 0
fi

echo "[error] No se pudo generar el PDF. Instala pandoc o Docker."
echo "        - pandoc: https://pandoc.org/installing.html"
echo "        - docker: https://docs.docker.com/get-docker/"
exit 1
