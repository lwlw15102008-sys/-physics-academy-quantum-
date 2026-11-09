"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import { BookOpen, ClipboardList, FileText, FlaskConical, LayoutDashboard, Settings, ShieldCheck, Trophy, Users, type LucideIcon } from "lucide-react";
import { SECTIONS, type SectionIcon } from "@/lib/sections";

const ICONS: Record<SectionIcon, LucideIcon> = {
  dashboard: LayoutDashboard,
  book: BookOpen,
  lessons: FileText,
  users: Users,
  quiz: ClipboardList,
  flask: FlaskConical,
  trophy: Trophy,
  settings: Settings,
};

const VERSION = process.env.NEXT_PUBLIC_APP_VERSION ?? "dev";

export default function AdminShell({ children, authEnforced }: { children: ReactNode; authEnforced: boolean }) {
  const pathname = usePathname();
  return (
    <div className="admin-shell">
      <aside className="side" aria-label="قائمة الإدارة">
        <div className="flex items-center gap-3 mb-10 w-full">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/logo-mark.svg" alt="" width={44} height={44} />
          <div>
            <b className="text-sm">PHYSICS ACADEMY</b>
            <div className="text-[11px] tracking-widest text-dim">CONTROL CENTER</div>
          </div>
        </div>
        <div className="text-[11px] text-dim mb-3 px-3 w-full">إدارة المنصة</div>
        <nav aria-label="أقسام الإدارة" className="w-full">
          {SECTIONS.map((s) => {
            const href = s.slug ? `/${s.slug}` : "/";
            const active = s.slug ? pathname === href : pathname === "/";
            const Icon = ICONS[s.icon];
            return (
              <Link key={s.slug || "home"} href={href} aria-current={active ? "page" : undefined} className={`nav ${active ? "active" : ""}`}>
                <Icon size={17} aria-hidden />
                {s.label}
              </Link>
            );
          })}
        </nav>
        <div className="panel p-4 mt-10 w-full">
          <ShieldCheck className="text-cyan-300" aria-hidden />
          <p className="text-xs font-bold mt-2">الأمان أولاً</p>
          <p className="text-[11px] muted leading-5 mt-1">
            {authEnforced ? "الوصول مقيّد بدور مدير/مالك عبر جلسة موثّقة." : "وضع التطوير: المصادقة معطّلة. في الإنتاج يُحجب الوصول بالكامل دون جلسة صالحة."}
          </p>
        </div>
      </aside>
      <main className="main">
        {!authEnforced && (
          <div role="alert" className="panel p-3 mb-5 text-xs text-amber-200">وضع التطوير — لا تنشر هذه اللوحة دون ضبط SUPABASE_JWT_SECRET (الإنتاج يفرض المصادقة تلقائياً).</div>
        )}
        {children}
        <footer className="text-center text-[11px] text-dim mt-10">PHYSICS ACADEMY · ADMIN FOUNDATION BUILD {VERSION}</footer>
      </main>
    </div>
  );
}
