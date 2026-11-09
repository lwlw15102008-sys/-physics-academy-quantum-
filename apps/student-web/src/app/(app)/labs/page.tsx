import Img from "@/components/Img";
import { labImage, LABS } from "@/lib/assets";

export const metadata = { title: "المختبرات | PHYSICS ACADEMY" };

export default function LabsPage() {
  return (
    <>
      <header className="mb-6">
        <div className="eyebrow">LABS</div>
        <h1 className="text-2xl md:text-3xl font-black mt-1">المختبرات والمحاكاة</h1>
        <p className="muted text-sm mt-2">اختر مختبراً. التجارب التفاعلية ستُفعَّل في مرحلة قادمة.</p>
      </header>
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-3">
        {LABS.map(({ slug, title, blurb }) => (
          <article key={slug} className="panel overflow-hidden">
            <Img src={labImage(slug)} alt="" className="w-full h-36 object-cover" />
            <div className="p-4">
              <h2 className="font-extrabold">{title}</h2>
              <p className="text-xs muted mt-1">{blurb}</p>
              <span className="text-[11px] text-dim mt-3 inline-block">قريباً</span>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}
