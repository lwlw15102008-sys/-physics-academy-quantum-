import { JwtError, verifyHs256Jwt } from "./jwt";
import { signToken } from "./test-utils";

const SECRET = "x".repeat(40);
const NOW = 1_800_000_000;
const good = { sub: "user-1", aud: "authenticated", exp: NOW + 600 };

function codeOf(fn: () => unknown): string {
  try {
    fn();
  } catch (e) {
    return e instanceof JwtError ? e.code : `OTHER:${String(e)}`;
  }
  return "NO_ERROR";
}

describe("verifyHs256Jwt", () => {
  it("accepts a valid token", () => {
    const p = verifyHs256Jwt(signToken(good, SECRET), SECRET, { audience: "authenticated", now: NOW });
    expect(p.sub).toBe("user-1");
  });

  it("rejects alg=none and other algorithms", () => {
    const none = `${Buffer.from('{"alg":"none"}').toString("base64url")}.${Buffer.from(JSON.stringify(good)).toString("base64url")}.`;
    expect(codeOf(() => verifyHs256Jwt(none, SECRET, { now: NOW }))).toBe("MALFORMED");
    const hs512 = signToken(good, SECRET, { alg: "HS512", typ: "JWT" });
    expect(codeOf(() => verifyHs256Jwt(hs512, SECRET, { now: NOW }))).toBe("BAD_ALG");
  });

  it("rejects a wrong secret and a tampered payload", () => {
    expect(codeOf(() => verifyHs256Jwt(signToken(good, "y".repeat(40)), SECRET, { now: NOW }))).toBe("BAD_SIGNATURE");
    const [h, , s] = signToken(good, SECRET).split(".");
    const forged = Buffer.from(JSON.stringify({ ...good, app_metadata: { role: "OWNER" } })).toString("base64url");
    expect(codeOf(() => verifyHs256Jwt(`${h}.${forged}.${s}`, SECRET, { now: NOW }))).toBe("BAD_SIGNATURE");
  });

  it("enforces exp (mandatory), nbf, audience and issuer", () => {
    expect(codeOf(() => verifyHs256Jwt(signToken({ ...good, exp: NOW - 60 }, SECRET), SECRET, { now: NOW }))).toBe("EXPIRED");
    expect(codeOf(() => verifyHs256Jwt(signToken({ sub: "u", aud: "authenticated" }, SECRET), SECRET, { now: NOW }))).toBe("BAD_CLAIMS");
    expect(codeOf(() => verifyHs256Jwt(signToken({ ...good, nbf: NOW + 600 }, SECRET), SECRET, { now: NOW }))).toBe("NOT_YET_VALID");
    expect(codeOf(() => verifyHs256Jwt(signToken({ ...good, aud: "other" }, SECRET), SECRET, { audience: "authenticated", now: NOW }))).toBe("BAD_AUDIENCE");
    expect(codeOf(() => verifyHs256Jwt(signToken(good, SECRET), SECRET, { issuer: "https://issuer.example", now: NOW }))).toBe("BAD_ISSUER");
  });

  it("rejects garbage input", () => {
    for (const bad of ["", "a.b", "a.b.c.d", "!!!.???.***", "x".repeat(9000)]) {
      expect(codeOf(() => verifyHs256Jwt(bad, SECRET, { now: NOW }))).toBe("MALFORMED");
    }
  });
});
