import Link from "next/link";

export default function NotFound() {
  return (
    <main className="min-h-screen grid place-items-center p-6 text-center">
      <div className="panel p-8 max-w-md">
        <h1 className="text-2xl font-black">الصفحة غير موجودة</h1>
        <p className="muted text-sm mt-3">تعذّر العثور على الصفحة المطلوبة.</p>
        <Link href="/" className="inline-block mt-5 rounded-xl bg-gradient-to-l from-blue-500 to-cyan-400 text-slate-950 font-extrabold px-5 py-3 text-sm">العودة للرئيسية</Link>
      </div>
    </main>
  );
}
