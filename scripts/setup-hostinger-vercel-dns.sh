#!/usr/bin/env bash
# Hostinger DNS for nexsocio.com → Vercel (run after adding domains in Vercel dashboard)
set -euo pipefail

cat <<'EOF'
Hostinger hPanel → Domains → nexsocio.com → DNS / DNS Zone

Add these records (remove conflicting A/CNAME for @ and www first):

┌─────────┬──────┬────────────────────────┬───────┐
│ Type    │ Name │ Value                  │ TTL   │
├─────────┼──────┼────────────────────────┼───────┤
│ A       │ @    │ 76.76.21.21            │ 14400 │
│ CNAME   │ www  │ cname.vercel-dns.com   │ 14400 │
└─────────┴──────┴────────────────────────┴───────┘

Notes:
  • @ = apex (nexsocio.com). Some panels label it blank or "NEXSOCIO".
  • www CNAME must NOT point to 76.76.21.21 — use cname.vercel-dns.com only.
  • DNS can take 5–60 minutes to propagate.

Vercel (after deploy):
  1. Project → Settings → Domains
  2. Add nexsocio.com and www.nexsocio.com
  3. Wait for "Valid Configuration" on both

Verify:
  dig nexsocio.com +short
  dig www.nexsocio.com +short
EOF