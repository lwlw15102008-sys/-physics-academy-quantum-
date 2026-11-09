import { NextResponse, type NextRequest } from "next/server";
import { hasAdminRole, verifyHs256Jwt } from "@/lib/jwt";

const COOKIE = "pa_session";

/** Production always enforces authentication. In development it can be switched on with ADMIN_REQUIRE_AUTH=true. */
function authEnforced(): boolean {
  return process.env.NODE_ENV === "production" || process.env.ADMIN_REQUIRE_AUTH === "true";
}

async function isAuthorized(req: NextRequest): Promise<boolean> {
  const secret = process.env.SUPABASE_JWT_SECRET?.trim();
  if (!secret || secret.length < 32) return false; // fail closed when not configured
  const token = req.cookies.get(COOKIE)?.value;
  if (!token) return false;
  try {
    return hasAdminRole(await verifyHs256Jwt(token, secret, { audience: "authenticated" }));
  } catch {
    return false;
  }
}

function buildCsp(nonce: string): string {
  const dev = process.env.NODE_ENV !== "production";
  let supabaseOrigin = "";
  try { supabaseOrigin = process.env.NEXT_PUBLIC_SUPABASE_URL ? new URL(process.env.NEXT_PUBLIC_SUPABASE_URL).origin : ""; } catch { supabaseOrigin = ""; }
  return [
    "default-src 'self'",
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'${dev ? " 'unsafe-eval'" : ""}`,
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: blob:",
    "font-src 'self' data:",
    `connect-src 'self'${supabaseOrigin ? ` ${supabaseOrigin}` : ""}${dev ? " ws:" : ""}`,
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    ...(dev ? [] : ["upgrade-insecure-requests"]),
  ].join("; ");
}

export async function middleware(req: NextRequest) {
  const nonce = btoa(crypto.randomUUID());
  const csp = buildCsp(nonce);

  if (authEnforced() && req.nextUrl.pathname !== "/login" && !(await isAuthorized(req))) {
    const url = req.nextUrl.clone();
    url.pathname = "/login";
    url.search = "";
    const redirect = NextResponse.redirect(url);
    redirect.headers.set("Content-Security-Policy", csp);
    redirect.headers.set("Cache-Control", "no-store");
    return redirect;
  }

  const headers = new Headers(req.headers);
  headers.set("x-nonce", nonce);
  headers.set("content-security-policy", csp);
  const res = NextResponse.next({ request: { headers } });
  res.headers.set("Content-Security-Policy", csp);
  res.headers.set("Cache-Control", "no-store");
  res.headers.set("X-Robots-Tag", "noindex, nofollow");
  return res;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|icon.svg|logo-mark.svg).*)"],
};
