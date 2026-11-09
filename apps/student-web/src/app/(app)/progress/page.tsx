import Img from "@/components/Img";
import { LEVELS, levelImage } from "@/lib/assets";

export const metadata = { title: "تقدّمي | PHYSICS ACADEMY" };

export default function ProgressPage() {
  return (
    <>
      <header className="mb-6">
        <div className="eyebrow">PROGRESS</div>
        <h1 className="text-2xl md:text-3xl font-black mt-1">تقدّمي وإنجازاتي</h1>
        <p className="muted text-sm mt-2">سلّم المستويات الخمسة عشر. مستواك الفعلي سيظهر بعد ربط حسابك بالخادم.</p>
      </header>
      <ol className="grid grid-cols-3 sm:grid-cols-5 gap-3" aria-label="مستويات المنصة">
        {LEVELS.map(({ n, slug, title }) => (
          <li key={n} className="panel p-3 text-center">
            <Img src={levelImage(n, slug)} alt={`شارة المستوى ${n}: ${title}`} className="w-20 h-20 mx-auto object-contain" />
            <div className="text-[11px] text-dim mt-2">المستوى {n}</div>
            <div className="font-bold text-sm">{title}</div>
          </li>
        ))}
      </ol>
    </>
  );
}
