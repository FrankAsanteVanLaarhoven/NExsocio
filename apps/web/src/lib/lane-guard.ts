/** Client-side mirror of lane_guard.py — personal posts must not carry business intent. */

const BUSINESS_INTENT_PATTERNS: RegExp[] = [
  /\b(buy\s+now|shop\s+now|order\s+now|dm\s+to\s+(buy|order)|link\s+in\s+bio)\b/i,
  /\b(for\s+sale|selling|on\s+sale|clearance|discount|%\s*off|promo\s*code)\b/i,
  /\b(book\s+now|hire\s+me|my\s+services|our\s+services|get\s+a\s+quote)\b/i,
  /\b(price|pricing|£\s*\d|€\s*\d|\$\s*\d|\d+\s*(gbp|usd|eur))\b/i,
  /\b(marketplace|listing|checkout|add\s+to\s+cart)\b/i,
  /\b(wholesale|retail|inventory|stock\s+left|limited\s+offer)\b/i,
  /\b(freelance|consulting|agency|startup|side\s*hustle)\b/i,
  /\b(commission|affiliate|sponsor\s+me|brand\s+deal)\b/i,
];

export function detectBusinessIntent(text: string): boolean {
  if (!text || text.trim().length < 8) return false;
  return BUSINESS_INTENT_PATTERNS.some((p) => p.test(text));
}

export const LANE_BUSINESS_HINT =
  "This looks like business content. Switch to the Business lane to sell, promote, or advertise.";