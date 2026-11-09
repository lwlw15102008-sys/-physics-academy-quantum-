'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { getSupabase } from '@/lib/supabase';

export default function AuthCallbackPage() {
  const router = useRouter();
  const [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const supabase = getSupabase();
        const code = new URLSearchParams(window.location.search).get('code');
        if (code) {
          const { error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);
          if (exchangeError) throw exchangeError;
        }
        const { data, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) throw sessionError;
        if (!data.session) throw new Error('لم يتم تأكيد جلسة Google. أعد المحاولة.');
        if (active) router.replace('/');
      } catch (e) {
        if (active) setError(e instanceof Error ? e.message : 'تعذر إكمال تسجيل الدخول.');
      }
    })();
    return () => { active = false; };
  }, [router]);
  return <main dir="rtl" className="min-h-screen grid place-items-center bg-[#080D1A] p-6 text-white"><div className="text-center"><p className="font-bold">{error ? 'تعذر تسجيل الدخول' : 'جارٍ تأكيد حساب Google…'}</p>{error && <><p className="mt-3 text-sm text-rose-300">{error}</p><button className="mt-5 rounded-xl bg-cyan-300 px-5 py-3 font-bold text-slate-950" onClick={() => router.replace('/login')}>العودة لتسجيل الدخول</button></>}</div></main>;
}
