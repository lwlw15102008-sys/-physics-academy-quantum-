export const SECTIONS = [
  { slug: "", label: "نظرة عامة", icon: "dashboard" },
  { slug: "curricula", label: "إدارة المناهج", icon: "book" },
  { slug: "lessons", label: "الدروس والمحتوى", icon: "lessons" },
  { slug: "people", label: "الطلاب والمعلمون", icon: "users" },
  { slug: "quizzes", label: "الاختبارات", icon: "quiz" },
  { slug: "labs", label: "المختبرات والمحاكاة", icon: "flask" },
  { slug: "rewards", label: "الإنجازات والمكافآت", icon: "trophy" },
  { slug: "settings", label: "الإعدادات", icon: "settings" },
] as const;

export type SectionIcon = (typeof SECTIONS)[number]["icon"];

export function findSection(slug: string) {
  return SECTIONS.find((s) => s.slug === slug && s.slug !== "");
}

/** Mirrors the middleware: production always enforces authentication. */
export function authEnforced(): boolean {
  return process.env.NODE_ENV === "production" || process.env.ADMIN_REQUIRE_AUTH === "true";
}
