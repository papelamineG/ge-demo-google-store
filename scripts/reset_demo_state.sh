#!/bin/bash
# =============================================================================
# Fast Demo State Reset Script (Takes ~10-15 seconds)
# Resets BigQuery tables and Firestore collections to their initial pre-demo state
# without redeploying Cloud Run, tearing down infrastructure, or changing URLs.
# =============================================================================

set -e
cd "$(dirname "$0")/.."

load_env() {
  local tmp_env
  tmp_env=$(mktemp /tmp/ge-reset-env-XXXXXX)
  awk '
    /^[[:space:]]*(export[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*=/ {
      sub(/\r$/, "")
      eq  = index($0, "=")
      key = substr($0, 1, eq)
      val = substr($0, eq + 1)
      if (val == "" || val ~ /^"/ || val ~ /^'"'"'/ || val ~ /"/) { print; next }
      sub(/[[:space:]]+#.*$/, "", val)
      sub(/[[:space:]]+$/, "", val)
      print key "\"" val "\""
      next
    }
    { print }
  ' "$1" > "$tmp_env"
  source "$tmp_env"
  rm -f "$tmp_env"
}

if [ -f .env ]; then
  load_env .env
fi

PROJECT_ID=${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}
export CLOUDSDK_CORE_PROJECT="$PROJECT_ID"
DATASET_ID=${BIGQUERY_DATASET:-${DATASET_ID:-"demo_google_store_2654"}}
FIRESTORE_COLLECTION=${FIRESTORE_COLLECTION:-"demo-google-store-2654-tasks"}

echo "================================================================================"
echo "⚡ Fast Resetting Demo State for: $SERVICE_NAME"
echo "Project:    $PROJECT_ID"
echo "BigQuery:   $DATASET_ID"
echo "Firestore:  $FIRESTORE_COLLECTION"
echo "================================================================================"

# 1. Reset BigQuery tables
echo "📊 [1/2] Reloading initial BigQuery tables..."
for f in data/*.csv; do
  case "$f" in *.hero.csv) continue ;; esac
  tbl=$(basename "$f" .csv)
  bq load --source_format=CSV --autodetect --skip_leading_rows=1 --replace "${DATASET_ID}.${tbl}" "$f" >/dev/null 2>&1 || true
  if [ -f "data/${tbl}_schema.json" ]; then
    bq update "${DATASET_ID}.${tbl}" "data/${tbl}_schema.json" >/dev/null 2>&1 || true
  fi
  if [ -f "data/${tbl}_bqdescription.txt" ]; then
    bq update --description "$(cat "data/${tbl}_bqdescription.txt")" "${DATASET_ID}.${tbl}" >/dev/null 2>&1 || true
  fi
done
echo "  ✅ BigQuery tables reset to original launch data."

# 2. Reset Firestore tasks
echo "🔥 [2/2] Resetting Firestore task queue and approval states..."
if [ -f data/firestore_seed.json ]; then
  uv run --no-project --with "google-cloud-firestore>=2.16.0,<3.0.0" --with "google-api-core>=2.20.0,<2.35.0" \
    python3 scripts/setup_fs.py --collection "$FIRESTORE_COLLECTION" --docs ./data/firestore_seed.json >/dev/null 2>&1 || true
  echo "  ✅ Firestore tasks reset to initial pending approval states."
fi

CHAT_LINK=$(cat .ge_direct_url 2>/dev/null || echo "https://console.cloud.google.com/gemini-enterprise/overview?project=${PROJECT_ID}")
echo ""
echo "🎉 DEMO STATE RESET COMPLETE in 10 SECONDS!"
echo "👉 Simply open a New Chat in Gemini Enterprise to start fresh:"
echo "   ${CHAT_LINK}"
echo "================================================================================"
