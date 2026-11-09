// Role names match the Prisma enum exactly (UPPER_CASE).
export type UserRole = "STUDENT" | "TEACHER" | "ADMIN" | "OWNER";
export type SubjectSlug = "physics" | "chemistry" | "biology" | "mathematics" | "geology";
export type SubscriptionTier = "FREE" | "PRO" | "VIP";

export interface SubjectDto {
  id: string;
  slug: SubjectSlug;
  title: string;
  description: string;
  sortOrder: number;
}

export interface LearningTask {
  id: string;
  title: string;
  subject: SubjectSlug;
  estimatedMinutes: number;
  status: "pending" | "in_progress" | "completed";
}

export interface ApiError {
  code: string;
  message: string;
  requestId?: string;
}

/** Every API failure is returned as { error: ApiError }. */
export interface ApiErrorResponse {
  error: ApiError;
}

export interface ApiDataResponse<T> {
  data: T;
  source?: string;
  persistent?: boolean;
}
