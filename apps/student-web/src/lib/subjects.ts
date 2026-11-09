export const SUBJECTS = [
  { slug: "physics", title: "الفيزياء", subtitle: "افهم قوانين الكون", color: "#3987FF", tag: "PHYSICS" },
  { slug: "chemistry", title: "الكيمياء", subtitle: "اكتشف عالم التفاعلات", color: "#35D5E8", tag: "CHEMISTRY" },
  { slug: "biology", title: "الأحياء", subtitle: "استكشف أسرار الحياة", color: "#35D39A", tag: "BIOLOGY" },
  { slug: "mathematics", title: "الرياضيات", subtitle: "حوّل الأرقام إلى أفكار", color: "#A78BFA", tag: "MATHEMATICS" },
  { slug: "geology", title: "الجيولوجيا", subtitle: "اقرأ تاريخ الأرض", color: "#FFBF69", tag: "GEOLOGY" },
] as const;

export type SubjectSlug = (typeof SUBJECTS)[number]["slug"];

export function findSubject(value: unknown) {
  return typeof value === "string" ? SUBJECTS.find((s) => s.slug === value) : undefined;
}
