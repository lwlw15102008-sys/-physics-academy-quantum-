import { createHmac, timingSafeEqual } from "node:crypto";

export type JwtErrorCode =
  | "MALFORMED"
  | "BAD_ALG"
  | "BAD_SIGNATURE"
  | "EXPIRED"
  | "NOT_YET_VALID"
  | "BAD_AUDIENCE"
  | "BAD_ISSUER"
  | "BAD_CLAIMS";

export class JwtError extends Error {
  constructor(public readonly code: JwtErrorCode) {
    super(code);
    this.name = "JwtError";
  }
}

export interface JwtPayload {
  sub?: unknown;
  aud?: unknown;
  iss?: unknown;
  exp?: unknown;
  nbf?: unknown;
  app_metadata?: { role?: unknown } | null;
  [claim: string]: unknown;
}

export interface VerifyOptions {
  audience?: string;
  issuer?: string | null;
  clockToleranceSec?: number;
  /** Seconds since epoch; injectable for tests. */
  now?: number;
}

const B64URL = /^[A-Za-z0-9_-]+$/;
const MAX_TOKEN_LENGTH = 8192;

function decodeJson(segment: string): Record<string, unknown> {
  if (!B64URL.test(segment)) throw new JwtError("MALFORMED");
  try {
    const parsed: unknown = JSON.parse(Buffer.from(segment, "base64url").toString("utf8"));
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) throw new JwtError("MALFORMED");
    return parsed as Record<string, unknown>;
  } catch (e) {
    if (e instanceof JwtError) throw e;
    throw new JwtError("MALFORMED");
  }
}

/**
 * Verifies an HS256 JWT. Only HS256 is accepted (never "none" or an algorithm named
 * by the attacker), the signature is compared in constant time, and `exp` is mandatory.
 */
export function verifyHs256Jwt(token: string, secret: string, options: VerifyOptions = {}): JwtPayload {
  if (typeof token !== "string" || token.length === 0 || token.length > MAX_TOKEN_LENGTH) throw new JwtError("MALFORMED");
  const parts = token.split(".");
  if (parts.length !== 3) throw new JwtError("MALFORMED");
  const [h, p, s] = parts;
  if (!B64URL.test(s)) throw new JwtError("MALFORMED");

  const header = decodeJson(h);
  if (header.alg !== "HS256" || (header.typ !== undefined && header.typ !== "JWT")) throw new JwtError("BAD_ALG");

  const expected = createHmac("sha256", secret).update(`${h}.${p}`).digest();
  const given = Buffer.from(s, "base64url");
  if (given.length !== expected.length || !timingSafeEqual(given, expected)) throw new JwtError("BAD_SIGNATURE");

  const payload = decodeJson(p) as JwtPayload;
  const now = options.now ?? Math.floor(Date.now() / 1000);
  const tol = options.clockToleranceSec ?? 5;

  if (typeof payload.exp !== "number" || !Number.isFinite(payload.exp)) throw new JwtError("BAD_CLAIMS");
  if (payload.exp + tol <= now) throw new JwtError("EXPIRED");
  if (payload.nbf !== undefined) {
    if (typeof payload.nbf !== "number" || !Number.isFinite(payload.nbf)) throw new JwtError("BAD_CLAIMS");
    if (payload.nbf - tol > now) throw new JwtError("NOT_YET_VALID");
  }
  if (options.audience !== undefined) {
    const aud = payload.aud;
    const ok = typeof aud === "string" ? aud === options.audience : Array.isArray(aud) && aud.includes(options.audience);
    if (!ok) throw new JwtError("BAD_AUDIENCE");
  }
  if (options.issuer) {
    if (payload.iss !== options.issuer) throw new JwtError("BAD_ISSUER");
  }
  return payload;
}
