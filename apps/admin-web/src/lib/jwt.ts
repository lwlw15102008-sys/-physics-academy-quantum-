// HS256 verification using WebCrypto so it runs in the Next.js Edge runtime (middleware).
// Mirrors services/api/src/auth/jwt.ts: HS256 only, mandatory exp, constant-time signature check.

export interface JwtPayload {
  sub?: unknown;
  aud?: unknown;
  exp?: unknown;
  nbf?: unknown;
  app_metadata?: { role?: unknown } | null;
  [claim: string]: unknown;
}

const B64URL = /^[A-Za-z0-9_-]+$/;
const MAX_TOKEN_LENGTH = 8192;

function b64urlToBytes(segment: string): Uint8Array {
  if (!B64URL.test(segment)) throw new Error("MALFORMED");
  const padded = segment.replace(/-/g, "+").replace(/_/g, "/") + "=".repeat((4 - (segment.length % 4)) % 4);
  const bin = atob(padded);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

function decodeJson(segment: string): Record<string, unknown> {
  const parsed: unknown = JSON.parse(new TextDecoder().decode(b64urlToBytes(segment)));
  if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error("MALFORMED");
  return parsed as Record<string, unknown>;
}

/** Resolves with the payload, or rejects with an Error for ANY problem (callers treat every error as "not authenticated"). */
export async function verifyHs256Jwt(token: string, secret: string, opts: { audience?: string; now?: number; clockToleranceSec?: number } = {}): Promise<JwtPayload> {
  if (!token || token.length > MAX_TOKEN_LENGTH) throw new Error("MALFORMED");
  const parts = token.split(".");
  if (parts.length !== 3) throw new Error("MALFORMED");
  const [h, p, s] = parts;

  const header = decodeJson(h);
  if (header.alg !== "HS256" || (header.typ !== undefined && header.typ !== "JWT")) throw new Error("BAD_ALG");

  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", enc.encode(secret) as unknown as BufferSource, { name: "HMAC", hash: "SHA-256" }, false, ["verify"]);
  const valid = await crypto.subtle.verify("HMAC", key, b64urlToBytes(s) as unknown as BufferSource, enc.encode(h + "." + p) as unknown as BufferSource);
  if (!valid) throw new Error("BAD_SIGNATURE");

  const payload = decodeJson(p) as JwtPayload;
  const now = opts.now ?? Math.floor(Date.now() / 1000);
  const tol = opts.clockToleranceSec ?? 5;
  if (typeof payload.exp !== "number" || !Number.isFinite(payload.exp)) throw new Error("BAD_CLAIMS");
  if (payload.exp + tol <= now) throw new Error("EXPIRED");
  if (payload.nbf !== undefined && (typeof payload.nbf !== "number" || payload.nbf - tol > now)) throw new Error("NOT_YET_VALID");
  if (opts.audience !== undefined) {
    const aud = payload.aud;
    const ok = typeof aud === "string" ? aud === opts.audience : Array.isArray(aud) && aud.includes(opts.audience);
    if (!ok) throw new Error("BAD_AUDIENCE");
  }
  return payload;
}

const ADMIN_ROLES = new Set(["ADMIN", "OWNER"]);

/** Role comes from app_metadata only (user_metadata is user-editable). */
export function hasAdminRole(payload: JwtPayload): boolean {
  const role = payload.app_metadata?.role;
  return typeof role === "string" && ADMIN_ROLES.has(role.toUpperCase());
}
