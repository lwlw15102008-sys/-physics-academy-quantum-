import Link from "next/link";
import { Atom, BookOpen, CalendarDays, ChevronLeft, Clock3, FlaskConical, GraduationCap, Sparkles, Target, Trophy } from "lucide-react";
import Img from "@/components/Img";
import SubjectsGrid from "@/components/SubjectsGrid";
import { TEACHER_IMAGE } from "@/lib/assets";

const STATS = [
  { icon: Clock3, label: "وقت التعلّم", value: "—", hint: "بانتظار ربط الحساب" },
  { icon: Target, label: "هدف اليوم", value: "غير محدد", hint: "اضبط هدفك لاحقاً" },
  { icon: Trophy, label: "إنجازاتك", value: "—", hint: "تُحسب من الخادم" },
  { icon: CalendarDays, label: "خطة الدراسة", value: "غير منشأة", hint: "مخطط المذاكرة" },
];

export default function HomePage() {
  return (
    <>
      <section className="panel p-6 md:p-9 relative overflow-hidden mb-7">
        <div className="absolute -left-12 -top-24 w-72 h-72 rounded-full bg-blue-500/10 blur-3xl" aria-hidden />
        <div className="relative max-w-2xl">
          <div className="eyebrow mb-3">YOUR PERSONAL LEARNING UNIVERSE</div>
          <h1 className="text-3xl md:text-4xl font-black leading-[1.55]">كل فكرة جديدة،<br /><span className="gradient-text">تفتح لك عالماً.</span></h1>
          <p className="muted text-sm leading-7 mt-3 max-w-xl">تعلّم بذكاء، جرّب بنفسك، واكتشف قدراتك خطوة بخطوة داخل تجربة علمية تفاعلية.</p>
          <div className="flex flex-wrap gap-3 mt-6">
            <Link href="/learn" className="rounded-xl bg-gradient-to-l from-blue-500 to-cyan-400 text-slate-950 font-extrabold px-5 py-3 text-sm flex items-center gap-2"><BookOpen size={17} aria-hidden /> ابدأ التعلّم <ChevronLeft size={17} aria-hidden /></Link>
            <Link href="/labs" className="rounded-xl border border-white/15 px-5 py-3 text-sm font-bold flex items-center gap-2"><FlaskConical size={17} aria-hidden /> استكشف المختبرات</Link>
          </div>
        </div>
        <div className="hidden lg:grid absolute left-12 top-1/2 -translate-y-1/2 w-48 h-48 rounded-full border border-blue-300/20 place-items-center" aria-hidden>
          <div className="w-36 h-36 rounded-full border border-cyan-300/30 grid place-items-center"><Atom size={82} strokeWidth={1} className="text-cyan-200 drop-shadow-[0_0_22px_#35d5e8]" /></div>
          <span className="absolute w-3 h-3 rounded-full bg-cyan-300 shadow-[0_0_20px_#35d5e8] top-5 right-7" />
        </div>
      </section>

      <section className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-8" aria-label="ملخص التقدم">
        {STATS.map(({ icon: Icon, label, value, hint }) => (
          <div className="panel p-4" key={label}>
            <div className="flex justify-between items-center"><span className="text-xs muted">{label}</span><Icon size={17} className="text-cyan-300" aria-hidden /></div>
            <div className="font-extrabold text-lg mt-3">{value}</div>
            <div className="text-[11px] text-dim mt-1">{hint}</div>
          </div>
        ))}
      </section>

      <SubjectsGrid />

      <section className="grid lg:grid-cols-2 gap-4">
        <div className="panel p-5 flex gap-4 items-center">
          <Img src={TEACHER_IMAGE} alt="المدرس الذكي كوانتا" className="w-24 h-24 object-contain shrink-0" />
          <div>
            <div className="flex items-center gap-2"><Sparkles className="text-violet-300" size={18} aria-hidden /><h3 className="font-extrabold">المدرس الذكي</h3></div>
            <p className="text-xs muted leading-6 mt-2">مدرسك الشخصي سيساعدك في فهم المفاهيم وحل المسائل وتحليل أخطائك. سيُفعَّل بعد ربط مزوّد الذكاء الاصطناعي عبر خادم آمن.</p>
            <div className="text-[11px] text-dim mt-2">قريباً</div>
          </div>
        </div>
        <div className="panel p-5">
          <div className="flex items-center gap-2"><GraduationCap className="text-blue-300" size={18} aria-hidden /><h3 className="font-extrabold">خطوتك القادمة</h3></div>
          <p className="text-xs muted leading-6 mt-3">ابدأ باختيار مادة دراسية. بعد توصيل حسابك ومحتوى المنهج سيقترح النظام الدرس التالي بناءً على تقدمك الفعلي.</p>
          <div className="progress-track mt-4" role="progressbar" aria-valuenow={0} aria-valuemin={0} aria-valuemax={100} aria-label="التقدم"><div className="progress-fill" style={{ width: "0%" }} /></div>
          <div className="text-[11px] text-dim mt-2">لا يوجد تقدم مسجل بعد — هذه معاينة وليست بيانات حقيقية.</div>
        </div>
      </section>
    </>
  );
}
