import { notFound } from "next/navigation";
import { findSection } from "@/lib/sections";

export default function SectionPage({ params }: { params: { section: string } }) {
  const section = findSection(params.section);
  if (!section) notFound();
  return (
    <>
      <header className="mb-8">
        <div className="text-xs muted">مركز التحكم / {section.label}</div>
        <h1 className="text-2xl font-black mt-1">{section.label}</h1>
      </header>
      <section className="panel p-6">
        <p className="text-sm muted leading-7">واجهة هذا القسم جاهزة كهيكل. ستُفعَّل عمليات الإدارة بعد توصيل قاعدة البيانات والتحقق من الصلاحيات على الخادم.</p>
      </section>
    </>
  );
}
