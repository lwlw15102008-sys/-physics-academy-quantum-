import { SetMetadata } from "@nestjs/common";
import type { UserRole } from "./auth.types";

export const IS_PUBLIC_KEY = "isPublic";
export const ROLES_KEY = "roles";

/** Opts a route out of the global authentication guard. Default is deny. */
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
/** Restricts a route to the given roles (authentication is still required). */
export const Roles = (...roles: UserRole[]) => SetMetadata(ROLES_KEY, roles);
