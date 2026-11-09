'use client';

import { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { getSupabase } from '@/lib/supabase';

export default function AuthGate({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let active = true;
    let subscription: { unsubscribe: () => void } | undefined;
    try {
      const supabase = getSupabase();
      supabase.auth.getSession().then(({ data }) => {
        if (!active) return;
        if (!data.session) router.replace(`/login?message=${encodeURIComponent('سجّل الدخول بحساب Google للمتابعة.')}`);
        else setReady(true);
      }).catch(() => { if (active) router.replace('/login'); });
      const { data } = supabase.auth.onAuthStateChange((_event, session) => {
        if (!session) router.replace('/login');
      });
      subscription = data.subscription;
    } catch {
      router.replace('/login?message=' + encodeURIComponent('يلزم إعداد تسجيل الدخول أولاً.'));
    }
    return () => { active = false; subscription?.unsubscribe(); };
  }, [pathname, router]);
  return ready ? children : <main className="min-h-screen grid place-items-center bg-[#080D1A] text-cyan-200" dir="rtl">جارٍ التحقق من تسجيل الدخول…</main>;
}
