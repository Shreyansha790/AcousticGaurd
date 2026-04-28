#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <file> [lines_per_chunk]" >&2
  exit 1
fi

FILE="$1"
LINES_PER_CHUNK="${2:-120}"

if [[ ! -f "$FILE" ]]; then
  echo "Error: file not found: $FILE" >&2
  exit 1
fi

if ! [[ "$LINES_PER_CHUNK" =~ ^[0-9]+$ ]] || [[ "$LINES_PER_CHUNK" -le 0 ]]; then
  echo "Error: lines_per_chunk must be a positive integer" >&2
  exit 1
fi

OUT_DIR="chat_chunks"
mkdir -p "$OUT_DIR"

base_name="$(basename "$FILE")"
name_without_ext="${base_name%.*}"
ext="${base_name##*.}"
if [[ "$ext" == "$base_name" ]]; then
  ext="txt"
fi

split -l "$LINES_PER_CHUNK" -d -a 3 "$FILE" "$OUT_DIR/${name_without_ext}_part_"

index=1
for f in "$OUT_DIR/${name_without_ext}_part_"*; do
  out="$f.$ext"
  mv "$f" "$out"
  echo "Created chunk $index: $out"
  index=$((index + 1))
done

echo "Done. Paste chunks in order with labels like Part 1/N, Part 2/N, ..."
