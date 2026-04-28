#!/usr/bin/env bash
set -euo pipefail

# Writes local config.js (gitignored) from environment variables.
# Usage:
#   TOMTOM_API_KEY=... FIREBASE_API_KEY=... FIREBASE_PROJECT_ID=... ./scripts/write_local_config.sh

EDGE_NODE_COUNT="${EDGE_NODE_COUNT:-2}"
TOMTOM_API_KEY="${TOMTOM_API_KEY:-}"
FIREBASE_API_KEY="${FIREBASE_API_KEY:-}"
FIREBASE_AUTH_DOMAIN="${FIREBASE_AUTH_DOMAIN:-}"
FIREBASE_PROJECT_ID="${FIREBASE_PROJECT_ID:-}"
FIREBASE_DATABASE_URL="${FIREBASE_DATABASE_URL:-}"
FIREBASE_STORAGE_BUCKET="${FIREBASE_STORAGE_BUCKET:-}"
FIREBASE_MESSAGING_SENDER_ID="${FIREBASE_MESSAGING_SENDER_ID:-}"
FIREBASE_APP_ID="${FIREBASE_APP_ID:-}"
FIREBASE_MEASUREMENT_ID="${FIREBASE_MEASUREMENT_ID:-}"
YAMNET_LOCAL_URL="${YAMNET_LOCAL_URL:-}"
YAMNET_REMOTE_URL="${YAMNET_REMOTE_URL:-}"
YAMNET_TIMEOUT_MS="${YAMNET_TIMEOUT_MS:-12000}"

cat > config.js <<CFG
window.ACOUSTIC_GUARD_CONFIG = {
  edgeNodeCount: ${EDGE_NODE_COUNT},
  firebase: {
    apiKey: "${FIREBASE_API_KEY}",
    authDomain: "${FIREBASE_AUTH_DOMAIN}",
    projectId: "${FIREBASE_PROJECT_ID}",
    databaseURL: "${FIREBASE_DATABASE_URL}",
    storageBucket: "${FIREBASE_STORAGE_BUCKET}",
    messagingSenderId: "${FIREBASE_MESSAGING_SENDER_ID}",
    appId: "${FIREBASE_APP_ID}",
    measurementId: "${FIREBASE_MEASUREMENT_ID}"
  },
  tomtomApiKey: "${TOMTOM_API_KEY}",
  yamnet: {
    localUrl: "${YAMNET_LOCAL_URL}",
    remoteUrl: "${YAMNET_REMOTE_URL}",
    timeoutMs: ${YAMNET_TIMEOUT_MS}
  }
};
CFG

echo "Wrote local config.js (gitignored)."
