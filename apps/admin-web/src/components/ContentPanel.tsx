"use client";

import { useMemo, useState } from "react";
import { Plus, Search } from "lucide-react";

const TRACKS = ["الفيزياء", "الكيمياء", "الأحياء", "الرياضيات", "الجيولوجيا"];

export default function ContentPanel() {
  const [search, setSearch] = useState("");
  const visible = useMemo(() => TRACKS.filter((t) => t.includes(search.trim())), [search]);
  return (
    <div className="panel p-5">
      <div className="flex flex-wrap justify-between items-center gap-3">
        <h3 className="font-extrabold">إدارة المحتوى</h3>
        <div className="flex gap-2">
          <label className="panel px-3 py-2 flex items-center gap-2">
            <Search size={16} aria-hidden />
            <span className="sr-only">ابحث في المحتوى</span>
            <input value={search} onChange={(e) => setSearch(e.target.value)} maxLength={40} placeholder="ابحث..." className="bg-transparent outline-none text-xs w-32 placeholder:text-dim" />
          </label>
          <button type="button" disabled title="يتطلب ربط قاعدة البيانات والصلاحيات" className="text-xs rounded-xl bg-blue-500 px-3 py-2 flex gap-2 items-center opacity-50 cursor-not-allowed">
            <Plus size={15} aria-hidden /> إضافة درس
          </button>
        </div>
      </div>
      <div className="mt-5 space-y-3">
        {visible.map((x) => (
          <div key={x} className="flex items-center justify-between border-b border-white/5 pb-3">
            <div>
              <b className="text-sm">{x}</b>
              <div className="text-[11px] muted mt-1">مسار دراسي · غير منشور</div>
            </div>
            <span className="tag">مسودة</span>
          </div>
        ))}
        {visible.length === 0 && <div className="text-xs muted">لا توجد نتائج.</div>}
      </div>
    </div>
  );
}
