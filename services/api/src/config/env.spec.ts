import { loadConfig, parseOrigins } from "./env";

const SECRET = "s".repeat(40);

describe("parseOrigins", () => {
  it("trims, normalises and de-duplicates", () => {
    expect(parseOrigins(" https://a.example/ , https://a.example,http://localhost:3000 ")).toEqual(["https://a.example", "http://localhost:3000"]);
  });
  it("rejects wildcard, null and non-http origins", () => {
    expect(() => parseOrigins("*")).toThrow();
    expect(() => parseOrigins("null")).toThrow();
    expect(() => parseOrigins("ftp://a.example")).toThrow();
    expect(() => parseOrigins("not a url")).toThrow();
  });
});

describe("loadConfig", () => {
  it("uses safe localhost defaults in development", () => {
    const c = loadConfig({ NODE_ENV: "development" });
    expect(c.corsOrigins).toEqual(["http://localhost:3000", "http://localhost:3001"]);
    expect(c.jwtSecret).toBeNull();
  });
  it("refuses unsafe production configuration", () => {
    expect(() => loadConfig({ NODE_ENV: "production", SUPABASE_JWT_SECRET: SECRET })).toThrow();
    expect(() => loadConfig({ NODE_ENV: "production", WEB_ORIGIN: "https://a.example" })).toThrow();
    expect(() => loadConfig({ NODE_ENV: "production", WEB_ORIGIN: "http://a.example", SUPABASE_JWT_SECRET: SECRET })).toThrow();
    expect(() => loadConfig({ NODE_ENV: "development", SUPABASE_JWT_SECRET: "short" })).toThrow();
  });
  it("accepts a valid production configuration", () => {
    const c = loadConfig({ NODE_ENV: "production", WEB_ORIGIN: "https://a.example", SUPABASE_JWT_SECRET: SECRET, PORT: "8080" });
    expect(c.port).toBe(8080);
    expect(c.corsOrigins).toEqual(["https://a.example"]);
  });
  it("validates numeric settings", () => {
    expect(() => loadConfig({ PORT: "99999" })).toThrow();
    expect(() => loadConfig({ THROTTLE_LIMIT: "abc" })).toThrow();
  });
});
