export type NodeEnv = "development" | "test" | "production";

export interface AppConfig {
  nodeEnv: NodeEnv;
  port: number;
  corsOrigins: string[];
  jwtSecret: string | null;
  jwtAudience: string;
  jwtIssuer: string | null;
  trustProxy: number | false;
  throttleLimit: number;
  throttleTtlMs: number;
}

export const APP_CONFIG = Symbol("APP_CONFIG");

const DEV_ORIGINS = ["http://localhost:3000", "http://localhost:3001"];

/** Parses a comma-separated allow-list. Wildcards and "null" are rejected on purpose. */
export function parseOrigins(raw: string | undefined): string[] {
  if (!raw) return [];
  const out: string[] = [];
  for (const item of raw.split(",")) {
    const value = item.trim();
    if (!value) continue;
    if (value === "*" || value.toLowerCase() === "null") {
      throw new Error(`WEB_ORIGIN must list explicit origins; "${value}" is not allowed`);
    }
    let url: URL;
    try {
      url = new URL(value);
    } catch {
      throw new Error(`WEB_ORIGIN contains an invalid origin: ${value}`);
    }
    if (url.protocol !== "https:" && url.protocol !== "http:") {
      throw new Error(`WEB_ORIGIN origin must be http(s): ${value}`);
    }
    out.push(url.origin);
  }
  return [...new Set(out)];
}

function intInRange(name: string, raw: string | undefined, fallback: number, min: number, max: number): number {
  if (raw === undefined || raw === "") return fallback;
  const n = Number(raw);
  if (!Number.isInteger(n) || n < min || n > max) {
    throw new Error(`${name} must be an integer between ${min} and ${max}`);
  }
  return n;
}

export function loadConfig(env: Record<string, string | undefined> = process.env): AppConfig {
  const rawEnv = env.NODE_ENV ?? "development";
  if (rawEnv !== "development" && rawEnv !== "test" && rawEnv !== "production") {
    throw new Error(`NODE_ENV must be development, test or production (got "${rawEnv}")`);
  }
  const nodeEnv: NodeEnv = rawEnv;
  const isProd = nodeEnv === "production";

  let corsOrigins = parseOrigins(env.WEB_ORIGIN);
  if (corsOrigins.length === 0) {
    if (isProd) throw new Error("WEB_ORIGIN is required in production (comma-separated https origins)");
    corsOrigins = DEV_ORIGINS;
  }
  if (isProd) {
    const insecure = corsOrigins.filter((o) => !o.startsWith("https://"));
    if (insecure.length > 0) throw new Error(`WEB_ORIGIN must use https in production: ${insecure.join(", ")}`);
  }

  const jwtSecret = env.SUPABASE_JWT_SECRET?.trim() ? env.SUPABASE_JWT_SECRET.trim() : null;
  if (jwtSecret !== null && jwtSecret.length < 32) {
    throw new Error("SUPABASE_JWT_SECRET must be at least 32 characters");
  }
  if (isProd && jwtSecret === null) throw new Error("SUPABASE_JWT_SECRET is required in production");

  const trustHops = intInRange("TRUST_PROXY_HOPS", env.TRUST_PROXY_HOPS, 0, 0, 10);

  return {
    nodeEnv,
    port: intInRange("PORT", env.PORT, 4000, 1, 65535),
    corsOrigins,
    jwtSecret,
    jwtAudience: env.JWT_AUDIENCE?.trim() || "authenticated",
    jwtIssuer: env.JWT_ISSUER?.trim() || null,
    trustProxy: trustHops > 0 ? trustHops : false,
    throttleLimit: intInRange("THROTTLE_LIMIT", env.THROTTLE_LIMIT, 100, 1, 100000),
    throttleTtlMs: intInRange("THROTTLE_TTL_MS", env.THROTTLE_TTL_MS, 60000, 1000, 3600000),
  };
}
