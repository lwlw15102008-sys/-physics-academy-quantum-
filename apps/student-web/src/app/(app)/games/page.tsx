import Img from "@/components/Img";
import { GAMES, gameImage } from "@/lib/assets";

export const metadata = { title: "الألعاب | PHYSICS ACADEMY" };

export default function GamesPage() {
  return (
    <>
      <header className="mb-6">
        <div className="eyebrow">GAMES</div>
        <h1 className="text-2xl md:text-3xl font-black mt-1">الألعاب والتحديات</h1>
        <p className="muted text-sm mt-2">تحديات تعليمية قصيرة. النتائج والنقاط ستُحسب على الخادم لاحقاً.</p>
      </header>
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-3">
        {GAMES.map(({ file, title, blurb }) => (
          <article key={file} className="panel overflow-hidden">
            <Img src={gameImage(file)} alt="" className="w-full aspect-video object-cover" />
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
