import { createHmac } from "node:crypto";

const b64 = (v: unknown) => Buffer.from(typeof v === "string" ? v : JSON.stringify(v)).toString("base64url");

/** Test helper: builds a signed HS256 token. */
export function signToken(payload: Record<string, unknown>, secret: string, header: Record<string, unknown> = { alg: "HS256", typ: "JWT" }): string {
  const h = b64(header);
  const p = b64(payload);
  const s = createHmac("sha256", secret).update(`${h}.${p}`).digest("base64url");
  return `${h}.${p}.${s}`;
}
