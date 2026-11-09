import { Activity, Atom, BookOpen, ClipboardList, Users } from "lucide-react";
import ContentPanel from "@/components/ContentPanel";

const METRICS = [
  { label: "إجمالي الطلاب", value: "—", hint: "بانتظار ربط قاعدة البيانات", icon: Users },
  { label: "الدروس المنشورة", value: "0", hint: "لا يوجد محتوى منشور بعد", icon: BookOpen },
  { label: "الاختبارات", value: "0", hint: "لم تتم إضافة اختبارات", icon: ClipboardList },
  { label: "نشاط المنصة", value: "—", hint: "التحليلات غير متصلة", icon: Activity },
];
const CHECKLIST = ["تفعيل تسجيل الدخول والأدوار", "استيراد المناهج ومراجعة مصادرها", "إضافة الدروس والوسائط التعليمية", "إعداد الاختبارات وبنك الأسئلة", "توصيل التحليلات والإشعارات", "اختبار صلاحيات لوحة الإدارة"];

export default function OverviewPage() {
  return (
    <>
      <header className="mb-8">
        <div className="text-xs muted">مركز التحكم / نظرة عامة</div>
        <h1 className="text-2xl font-black mt-1">نظرة عامة</h1>
      </header>
      <section className="panel p-6 mb-6 relative overflow-hidden">
        <div className="relative z-10 max-w-xl">
          <span className="tag">ADMIN CONSOLE · FOUNDATION</span>
          <h2 className="text-2xl font-black mt-4">إدارة عالم التعلّم من مكان واحد</h2>
          <p className="text-sm muted leading-7 mt-2">تحكّم في المناهج والدروس والطلاب والاختبارات والتجارب العلمية، مع متابعة الأداء والجودة. لا توجد بيانات حقيقية قبل ربط قاعدة البيانات.</p>
        </div>
        <Atom className="absolute left-10 top-1/2 -translate-y-1/2 text-blue-400/20" size={130} aria-hidden />
      </section>
      <section className="grid sm:grid-cols-2 xl:grid-cols-4 gap-3 mb-7" aria-label="المؤشرات">
        {METRICS.map(({ label, value, hint, icon: Icon }) => (
          <div key={label} className="panel p-5">
            <div className="flex justify-between"><span className="text-xs muted">{label}</span><Icon className="text-cyan-300" size={19} aria-hidden /></div>
            <div className="metric mt-3">{value}</div>
            <div className="text-[11px] muted mt-1">{hint}</div>
          </div>
        ))}
      </section>
      <section className="grid xl:grid-cols-2 gap-4">
        <ContentPanel />
        <div className="panel p-5">
          <h3 className="font-extrabold">قائمة تجهيز الإطلاق</h3>
          <ol className="mt-5 space-y-4 text-xs">
            {CHECKLIST.map((x, i) => (
              <li className="flex gap-3 items-center" key={x}>
                <span className="w-6 h-6 rounded-full bg-blue-500/20 text-cyan-200 grid place-items-center" aria-hidden>{i + 1}</span>
                <span className="muted">{x}</span>
              </li>
            ))}
          </ol>
        </div>
      </section>
    </>
  );
}
