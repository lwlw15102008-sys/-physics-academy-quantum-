import Link from "next/link";
import ComingSoon from "@/components/ComingSoon";
import { findSubject, SUBJECTS } from "@/lib/subjects";

export const metadata = { title: "تعلّم | PHYSICS ACADEMY" };

export default function LearnPage({ searchParams }: { searchParams: { subject?: string | string[] } }) {
  // Only whitelisted slugs are ever used; anything else is ignored.
  const raw = Array.isArray(searchParams.subject) ? searchParams.subject[0] : searchParams.subject;
  const subject = findSubject(raw);
  return (
    <ComingSoon eyebrow="LEARN" title={subject ? `مادة ${subject.title}` : "المواد الدراسية"}>
      <div className="flex flex-wrap gap-2 mt-6">
        {SUBJECTS.map((s) => (
          <Link key={s.slug} href={`/learn?subject=${s.slug}`} aria-current={subject?.slug === s.slug ? "true" : undefined} className={`rounded-xl border px-4 py-2 text-sm ${subject?.slug === s.slug ? "border-cyan-300 text-cyan-200" : "border-white/15"}`}>{s.title}</Link>
        ))}
      </div>
    </ComingSoon>
  );
}
