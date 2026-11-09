"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ChevronLeft, Search } from "lucide-react";
import Img from "@/components/Img";
import { subjectImage } from "@/lib/assets";
import { fetchSubjects } from "@/lib/api";
import { normalizeArabic } from "@/lib/arabic";
import { SUBJECTS } from "@/lib/subjects";

export default function SubjectsGrid() {
  const [query, setQuery] = useState("");
  const [api, setApi] = useState<"checking" | "ok" | "down">("checking");

  useEffect(() => {
    let alive = true;
    fetchSubjects().then((subjects) => {
      if (alive) setApi(subjects ? "ok" : "down");
    });
    return () => {
      alive = false;
    };
  }, []);

  const visible = useMemo(() => {
    const q = normalizeArabic(query);
    if (!q) return SUBJECTS;
    return SUBJECTS.filter((s) => normalizeArabic(s.title).includes(q) || s.tag.toLowerCase().includes(q));
  }, [query]);

  return (
    <section className="mb-8" aria-labelledby="subjects-heading">
      <div className="flex flex-wrap items-end justify-between gap-3 mb-4">
        <div>
          <div className="eyebrow">EXPLORE KNOWLEDGE</div>
          <h2 id="subjects-heading" className="text-xl font-extrabold mt-1">المواد الدراسية</h2>
        </div>
        <label className="flex items-center gap-2 panel px-3 py-2 w-full sm:w-64">
          <Search size={16} className="text-dim" aria-hidden />
          <span className="sr-only">ابحث عن مادة</span>
          <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="ابحث عن مادة..." maxLength={40} className="bg-transparent outline-none text-xs w-full placeholder:text-dim" />
        </label>
      </div>
      <p className="text-[11px] text-dim mb-3" role="status">
        {api === "checking" && "جارٍ فحص الاتصال بالخادم…"}
        {api === "ok" && "الخادم متصل (بيانات تجريبية غير محفوظة)."}
        {api === "down" && "الخادم غير متاح حالياً — تُعرض المواد من الإعدادات المحلية."}
      </p>
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-3">
        {visible.map(({ slug, title, subtitle, color, tag }) => (
          <Link key={slug} href={`/learn?subject=${slug}`} className="panel subject-card overflow-hidden text-right">
            <div className="relative h-36">
              <Img src={subjectImage(slug)} alt="" className="absolute inset-0 w-full h-full object-cover" />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0E182B] via-transparent to-transparent" aria-hidden />
              <span className="absolute top-3 left-3 text-[11px] tracking-[2px] text-white/80">{tag}</span>
            </div>
            <div className="p-4">
              <div className="font-extrabold text-lg" style={{ color }}>{title}</div>
              <div className="text-xs muted mt-1">{subtitle}</div>
              <div className="flex justify-between items-center mt-3">
                <span className="text-[11px] text-dim">المحتوى قيد الإعداد</span>
                <ChevronLeft size={18} aria-hidden />
              </div>
            </div>
          </Link>
        ))}
      </div>
      {visible.length === 0 && <div className="panel p-6 text-center muted text-sm mt-3">لا توجد مادة مطابقة لبحثك.</div>}
    </section>
  );
}
