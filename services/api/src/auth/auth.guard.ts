import {
  CanActivate,
  ExecutionContext,
  ForbiddenException,
  Inject,
  Injectable,
  ServiceUnavailableException,
  UnauthorizedException,
} from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { APP_CONFIG, AppConfig } from "../config/env";
import { AuthedRequest, UserRole, parseRole } from "./auth.types";
import { IS_PUBLIC_KEY, ROLES_KEY } from "./decorators";
import { JwtError, verifyHs256Jwt } from "./jwt";

/** Global guard: every route requires a valid bearer token unless marked @Public(). */
@Injectable()
export class AuthGuard implements CanActivate {
  constructor(
    private readonly reflector: Reflector,
    @Inject(APP_CONFIG) private readonly config: AppConfig,
  ) {}

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [context.getHandler(), context.getClass()]);
    if (isPublic) return true;

    // Fail closed: without a configured secret nobody is authenticated.
    if (!this.config.jwtSecret) {
      throw new ServiceUnavailableException({ code: "AUTH_NOT_CONFIGURED", message: "Authentication is not configured" });
    }

    const request = context.switchToHttp().getRequest<AuthedRequest>();
    const header = request.headers.authorization;
    const match = typeof header === "string" ? /^Bearer ([A-Za-z0-9._-]+)$/.exec(header) : null;
    if (!match) throw new UnauthorizedException({ code: "MISSING_TOKEN", message: "Bearer token required" });

    try {
      const payload = verifyHs256Jwt(match[1], this.config.jwtSecret, {
        audience: this.config.jwtAudience,
        issuer: this.config.jwtIssuer,
      });
      if (typeof payload.sub !== "string" || payload.sub.length === 0 || payload.sub.length > 128) {
        throw new JwtError("BAD_CLAIMS");
      }
      // Role is read from app_metadata only: user_metadata is user-editable and must never grant privileges.
      request.user = { id: payload.sub, role: parseRole(payload.app_metadata?.role) };
    } catch {
      throw new UnauthorizedException({ code: "INVALID_TOKEN", message: "Invalid or expired token" });
    }
    return true;
  }
}

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const required = this.reflector.getAllAndOverride<UserRole[] | undefined>(ROLES_KEY, [context.getHandler(), context.getClass()]);
    if (!required || required.length === 0) return true;
    const user = context.switchToHttp().getRequest<AuthedRequest>().user;
    if (!user || !required.includes(user.role)) {
      throw new ForbiddenException({ code: "FORBIDDEN", message: "Insufficient permissions" });
    }
    return true;
  }
}
