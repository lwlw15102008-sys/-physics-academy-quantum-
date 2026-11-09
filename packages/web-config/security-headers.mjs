// Shared HTTP security headers for the Next.js apps.
// CSP note: Next 14 emits inline bootstrap scripts, so a static CSP needs 'unsafe-inline' for scripts.
// The admin app does not use this CSP: its middleware issues a per-request nonce instead.

/** @param {string | undefined} apiUrl e.g. https://api.example.com/api/v1 */
export function originOf(apiUrl) {
  if (!apiUrl) return null;
  try {
    return new URL(apiUrl).origin;
  } catch {
    return null;
  }
}

/** @param {{ apiOrigin?: string | null, supabaseOrigin?: string | null, isDev?: boolean, withCsp?: boolean }} opts */
export function buildSecurityHeaders({ apiOrigin = null, supabaseOrigin = null, isDev = false, withCsp = true } = {}) {
  const headers = [
    { key: "X-Content-Type-Options", value: "nosniff" },
    { key: "X-Frame-Options", value: "DENY" },
    { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
    { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(), payment=()" },
    { key: "Cross-Origin-Opener-Policy", value: "same-origin" },
    { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  ];
  if (withCsp) {
    const connect = ["'self'", apiOrigin, supabaseOrigin, isDev ? "ws:" : null].filter(Boolean).join(" ");
    const csp = [
      "default-src 'self'",
      `script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ""}`,
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: blob:",
      "font-src 'self' data:",
      `connect-src ${connect}`,
      "object-src 'none'",
      "base-uri 'self'",
      "form-action 'self'",
      "frame-ancestors 'none'",
      ...(isDev ? [] : ["upgrade-insecure-requests"]),
    ].join("; ");
    headers.push({ key: "Content-Security-Policy", value: csp });
  }
  return headers;
}
