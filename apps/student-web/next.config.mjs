import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildSecurityHeaders, originOf } from "../../packages/web-config/security-headers.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const pkg = JSON.parse(fs.readFileSync(path.join(dir, "package.json"), "utf8"));
const isDev = process.env.NODE_ENV !== "production";
const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? (isDev ? "http://localhost:4000/api/v1" : undefined);

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  reactStrictMode: true,
  poweredByHeader: false,
  transpilePackages: ["@physics-academy/shared-types", "@physics-academy/design-tokens"],
  experimental: { outputFileTracingRoot: path.join(dir, "../../") },
  env: { NEXT_PUBLIC_APP_VERSION: pkg.version },
  async headers() {
    return [{ source: "/(.*)", headers: buildSecurityHeaders({ apiOrigin: originOf(apiUrl), supabaseOrigin: originOf(process.env.NEXT_PUBLIC_SUPABASE_URL), isDev }) }];
  },
};
export default nextConfig;
