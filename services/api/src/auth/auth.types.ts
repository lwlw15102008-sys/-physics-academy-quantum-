import type { Request } from "express";

export type UserRole = "STUDENT" | "TEACHER" | "ADMIN" | "OWNER";
export const USER_ROLES: readonly UserRole[] = ["STUDENT", "TEACHER", "ADMIN", "OWNER"];

export interface AuthUser {
  id: string;
  role: UserRole;
}

export interface AuthedRequest extends Request {
  user?: AuthUser;
}

/** Unknown or missing roles collapse to the least-privileged role. */
export function parseRole(value: unknown): UserRole {
  if (typeof value !== "string") return "STUDENT";
  const upper = value.toUpperCase();
  return (USER_ROLES as readonly string[]).includes(upper) ? (upper as UserRole) : "STUDENT";
}
