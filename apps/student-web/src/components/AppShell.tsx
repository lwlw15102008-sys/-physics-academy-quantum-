"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";
import { Bell, BookOpen, ChevronLeft, FlaskConical, Gamepad2, Home, Sparkles, Trophy, User, type LucideIcon } from "lucide-react";

const NAV: { href: string; label: string; icon: LucideIcon }[] = [
  { href: "/", label: "الرئيسية", icon: Home },
  { href: "/learn", label: "تعلّم", icon: BookOpen },
  { href: "/labs", label: "المختبرات", icon: FlaskConical },
  { href: "/games", label: "الألعاب", icon: Gamepad2 },
  { href: "/progress", label: "تقدّمي", icon: Trophy },
];

const VERSION = process.env.NEXT_PUBLIC_APP_VERSION ?? "dev";

function isActive(pathname: string, href: string) {
  return href === "/" ? pathname === "/" : pathname === href || pathname.startsWith(`${href}/`);
}

export default function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const [today, setToday] = useState("");
  const [showNotifications, setShowNotifications] = useState(false);

  // Computed on the client so it is always the real current date (and never a hydration mismatch).
  useEffect(() => {
    setToday(new Intl.DateTimeFormat("ar-EG-u-nu-latn", { weekday: "long", day: "numeric", month: "long", year: "numeric" }).format(new Date()));
  }, []);

  return (
    <div className="shell">
      <aside className="sidebar" aria-label="القائمة الرئيسية">
        <Link href="/" className="flex items-center gap-3 mb-12 px-2" aria-label="PHYSICS ACADEMY — الرئيسية">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/logo-mark.svg" alt="" width={42} height={42} />
          <div>
            <div className="font-black text-[15px] tracking-wide">PHYSICS <span className="gradient-text">ACADEMY</span></div>
            <div className="text-[11px] text-dim tracking-[2px]">QUANTUM UNIVERSE</div>
          </div>
        </Link>
        <div className="eyebrow px-3 mb-3">مساحة التعلّم</div>
        <nav className="space-y-2" aria-label="التنقل">
          {NAV.map(({ href, label, icon: Icon }) => {
            const active = isActive(pathname, href);
            return (
              <Link key={href} href={href} aria-current={active ? "page" : undefined} className={`nav-link w-full ${active ? "active" : ""}`}>
                <Icon size={18} aria-hidden />
                <span>{label}</span>
                {active && <ChevronLeft className="mr-auto" size={15} aria-hidden />}
              </Link>
            );
          })}
        </nav>
        <div className="panel p-4 mt-12">
          <div className="flex items-center gap-2 text-sm font-bold"><Sparkles size={16} className="text-cyan-300" aria-hidden /> مساحة الاستكشاف</div>
          <p className="text-xs muted leading-6 mt-2">تجارب ومحاكاة تساعدك على فهم العلوم بالتفاعل.</p>
          <Link href="/labs" className="text-xs text-cyan-300 mt-2 inline-block">اكتشف المختبرات ←</Link>
        </div>
        <div className="mt-auto pt-6 text-[11px] text-dim">نسخة تأسيسية {VERSION}</div>
      </aside>

      <main className="main">
        <header className="flex items-center justify-between gap-4 mb-9">
          <div>
            <div className="text-xs muted min-h-[1rem]">{today}</div>
            <div className="text-lg font-extrabold">مرحباً بك في عالمك العلمي</div>
          </div>
          <div className="relative flex items-center gap-2">
            <button
              type="button"
              onClick={() => setShowNotifications((v) => !v)}
              aria-label="الإشعارات"
              aria-expanded={showNotifications}
              aria-controls="notifications-panel"
              className="panel p-3"
            >
              <Bell size={17} aria-hidden />
            </button>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-violet-600 grid place-items-center" role="img" aria-label="الحساب">
              <User size={18} aria-hidden />
            </div>
            {showNotifications && (
              <div id="notifications-panel" role="status" className="panel absolute top-14 left-0 w-64 p-4 text-sm z-30">
                لا توجد إشعارات. ستظهر هنا بعد ربط حساب الطالب بالخادم.
              </div>
            )}
          </div>
        </header>
        {children}
        <footer className="text-center text-[11px] text-dim mt-10">PHYSICS ACADEMY · QUANTUM LEARNING UNIVERSE · FOUNDATION BUILD {VERSION}</footer>
      </main>

      <nav className="bottom-nav" aria-label="التنقل السفلي">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = isActive(pathname, href);
          return (
            <Link key={href} href={href} aria-current={active ? "page" : undefined} className={`flex flex-col items-center gap-1 text-[11px] px-2 ${active ? "text-cyan-300" : "text-slate-400"}`}>
              <Icon size={19} aria-hidden />
              {label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
