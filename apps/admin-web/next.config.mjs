import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildSecurityHeaders } from "../../packages/web-config/security-headers.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const pkg = JSON.parse(fs.readFileSync(path.join(dir, "package.json"), "utf8"));

/** @type {import("next").NextConfig} */
const nextConfig = {
  output: "standalone",
  reactStrictMode: true,
  poweredByHeader: false,
  transpilePackages: ["@physics-academy/design-tokens"],
  experimental: { outputFileTracingRoot: path.join(dir, "../../") },
  env: { NEXT_PUBLIC_APP_VERSION: pkg.version },
  // The Content-Security-Policy (with a per-request nonce) is issued by src/middleware.ts.
  async headers() {
    return [{ source: "/(.*)", headers: buildSecurityHeaders({ withCsp: false }) }];
  },
};
export default nextConfig;
