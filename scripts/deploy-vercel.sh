#!/usr/bin/env bash
# Deploy NEXSOCIO web (apps/web) to Vercel with nexsocio.com
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WEB="${ROOT}/apps/web"

echo "NEXSOCIO → Vercel production deploy"
echo "  Root directory: apps/web"
echo "  Domain:         nexsocio.com"
echo ""

if ! command -v vercel >/dev/null 2>&1; then
  echo "Installing Vercel CLI..."
  npm install -g vercel
fi

cd "${WEB}"

if [[ ! -d .vercel ]]; then
  echo "Linking Vercel project (first run)..."
  vercel link
fi

if [[ "${1:-}" == "--sync-env" ]]; then
  "${ROOT}/scripts/vercel-env-sync.sh"
fi

echo "Deploying to production..."
vercel deploy --prod --yes

echo ""
echo "Add domains in Vercel (if not linked to GitHub yet):"
echo "  vercel domains add nexsocio.com"
echo "  vercel domains add www.nexsocio.com"
echo ""
"${ROOT}/scripts/setup-hostinger-vercel-dns.sh"
echo ""
echo "Sync env vars: ./scripts/deploy-vercel.sh --sync-env"