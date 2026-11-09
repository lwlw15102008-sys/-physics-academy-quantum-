import type { ReactNode } from "react";

export default function ComingSoon({ eyebrow, title, children }: { eyebrow: string; title: string; children?: ReactNode }) {
  return (
    <section className="panel p-6 md:p-9">
      <div className="eyebrow mb-3">{eyebrow}</div>
      <h1 className="text-2xl md:text-3xl font-black">{title}</h1>
      <p className="muted text-sm leading-7 mt-3 max-w-xl">هذا القسم ضمن هيكل الواجهة، وسيتم ربط محتواه بعد إعداد قاعدة البيانات وحساب الطالب.</p>
      {children}
    </section>
  );
}
