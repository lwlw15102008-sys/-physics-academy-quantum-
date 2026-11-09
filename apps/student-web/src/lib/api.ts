import type { ApiDataResponse, SubjectDto } from "@physics-academy/shared-types";

/** Returns the API base URL, or null when it is not configured (always required in production). */
export function getApiBase(): string | null {
  const raw = process.env.NEXT_PUBLIC_API_URL ?? (process.env.NODE_ENV !== "production" ? "http://localhost:4000/api/v1" : undefined);
  if (!raw) return null;
  try {
    const url = new URL(raw);
    if (url.protocol !== "https:" && url.protocol !== "http:") return null;
    return url.toString().replace(/\/$/, "");
  } catch {
    return null;
  }
}

function isSubjectDto(v: unknown): v is SubjectDto {
  if (typeof v !== "object" || v === null) return false;
  const o = v as Record<string, unknown>;
  return typeof o.id === "string" && typeof o.slug === "string" && typeof o.title === "string" && typeof o.description === "string";
}

/** Fetches the subject catalogue with a timeout; any failure or unexpected shape yields null. */
export async function fetchSubjects(timeoutMs = 5000): Promise<SubjectDto[] | null> {
  const base = getApiBase();
  if (!base) return null;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(`${base}/catalog/subjects`, { signal: controller.signal, credentials: "omit", headers: { Accept: "application/json" } });
    if (!res.ok) return null;
    const body = (await res.json()) as Partial<ApiDataResponse<unknown>>;
    if (!Array.isArray(body.data) || !body.data.every(isSubjectDto)) return null;
    return body.data;
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}
