#!/bin/bash

# QuantumNews automation: run fast tests and verify Cloudflare tunnel health.
# This script does NOT start any local servers.

set -euo pipefail

PROJECT_DIR="/Users/joelchu/quantum-webscraper"
DOMAIN="https://quantumnews-ps23.3jcllc.com"

echo "🔎 Running tests (scoped, no plugin autoload)..."
cd "$PROJECT_DIR"
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
python3 -m pytest -q "$PROJECT_DIR/test_alpha_vantage.py" || {
  echo "❌ Tests failed"; exit 1;
}

echo "\n🌐 Checking remote health via Cloudflare named tunnel..."
set +e
curl -sS "$DOMAIN/health" | sed -e 's/{/{\n  /' -e 's/,/,\n  /g' -e 's/}/\n}/'
STATUS=$?
set -e

if [ $STATUS -ne 0 ]; then
  echo "❗ Could not reach $DOMAIN/health. Ensure the remote server and tunnel are running."
  exit 2
fi

echo "\n✅ Done."

