import { ExecutionContext, ForbiddenException, ServiceUnavailableException, UnauthorizedException } from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { AppConfig } from "../config/env";
import { AuthGuard, RolesGuard } from "./auth.guard";
import { IS_PUBLIC_KEY, ROLES_KEY } from "./decorators";
import { signToken } from "./test-utils";

const SECRET = "z".repeat(40);
const config: AppConfig = {
  nodeEnv: "test", port: 4000, corsOrigins: [], jwtSecret: SECRET, jwtAudience: "authenticated",
  jwtIssuer: null, trustProxy: false, throttleLimit: 100, throttleTtlMs: 60000,
};
const exp = () => Math.floor(Date.now() / 1000) + 600;

function ctx(headers: Record<string, string>, meta: Record<string, unknown> = {}) {
  const req: Record<string, unknown> = { headers };
  const reflector = { getAllAndOverride: (key: string) => meta[key] } as unknown as Reflector;
  const context = {
    getHandler: () => () => undefined,
    getClass: () => class {},
    switchToHttp: () => ({ getRequest: () => req }),
  } as unknown as ExecutionContext;
  return { req, reflector, context };
}

describe("AuthGuard", () => {
  it("lets @Public routes through without a token", () => {
    const { reflector, context } = ctx({}, { [IS_PUBLIC_KEY]: true });
    expect(new AuthGuard(reflector, config).canActivate(context)).toBe(true);
  });
  it("rejects requests without or with an invalid token", () => {
    const a = ctx({});
    expect(() => new AuthGuard(a.reflector, config).canActivate(a.context)).toThrow(UnauthorizedException);
    const b = ctx({ authorization: "Bearer not.a.token" });
    expect(() => new AuthGuard(b.reflector, config).canActivate(b.context)).toThrow(UnauthorizedException);
  });
  it("fails closed when no secret is configured", () => {
    const { reflector, context } = ctx({ authorization: "Bearer a.b.c" });
    expect(() => new AuthGuard(reflector, { ...config, jwtSecret: null }).canActivate(context)).toThrow(ServiceUnavailableException);
  });
  it("derives the role from app_metadata only, defaulting to STUDENT", () => {
    const token = signToken({ sub: "u1", aud: "authenticated", exp: exp(), app_metadata: { role: "admin" }, user_metadata: { role: "OWNER" } }, SECRET);
    const a = ctx({ authorization: `Bearer ${token}` });
    expect(new AuthGuard(a.reflector, config).canActivate(a.context)).toBe(true);
    expect(a.req.user).toEqual({ id: "u1", role: "ADMIN" });
    const plain = signToken({ sub: "u2", aud: "authenticated", exp: exp(), user_metadata: { role: "OWNER" } }, SECRET);
    const b = ctx({ authorization: `Bearer ${plain}` });
    new AuthGuard(b.reflector, config).canActivate(b.context);
    expect(b.req.user).toEqual({ id: "u2", role: "STUDENT" });
  });
});

describe("RolesGuard", () => {
  it("enforces required roles", () => {
    const allowed = ctx({}, { [ROLES_KEY]: ["ADMIN", "OWNER"] });
    allowed.req.user = { id: "u", role: "ADMIN" };
    expect(new RolesGuard(allowed.reflector).canActivate(allowed.context)).toBe(true);
    const denied = ctx({}, { [ROLES_KEY]: ["ADMIN", "OWNER"] });
    denied.req.user = { id: "u", role: "STUDENT" };
    expect(() => new RolesGuard(denied.reflector).canActivate(denied.context)).toThrow(ForbiddenException);
  });
});
