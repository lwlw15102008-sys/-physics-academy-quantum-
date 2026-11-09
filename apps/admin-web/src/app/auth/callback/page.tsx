'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@supabase/supabase-js';

export default function AdminAuthCallback() {
  const router = useRouter();
  const [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
        const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
        if (!url || !key) throw new Error('إعدادات Supabase غير مكتملة.');
        const supabase = createClient(url, key, { auth: { flowType: 'pkce', persistSession: true, detectSessionInUrl: false } });
        const code = new URLSearchParams(window.location.search).get('code');
        if (code) {
          const { error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);
          if (exchangeError) throw exchangeError;
        }
        const { data, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) throw sessionError;
        const token = data.session?.access_token;
        if (!token) throw new Error('لم يتم استلام جلسة Google. أعد المحاولة.');
        const role = data.session?.user.app_metadata?.role;
        if (!['ADMIN', 'OWNER'].includes(String(role).toUpperCase())) {
          await supabase.auth.signOut();
          throw new Error('هذا الحساب غير مصرح له بدخول لوحة الإدارة.');
        }
        document.cookie = `pa_session=${token}; Path=/; Max-Age=3600; SameSite=Lax${location.protocol === 'https:' ? '; Secure' : ''}`;
        if (active) router.replace('/');
      } catch (e) { if (active) setError(e instanceof Error ? e.message : 'تعذر تأكيد صلاحية الحساب.'); }
    })();
    return () => { active = false; };
  }, [router]);
  return <main dir="rtl" className="min-h-screen grid place-items-center p-6 text-white"><div className="text-center">{error ? <><p className="text-rose-300">{error}</p><button className="mt-5 rounded-xl bg-cyan-300 px-5 py-3 font-bold text-slate-950" onClick={() => router.replace('/login')}>العودة</button></> : 'جارٍ التحقق من حساب Google وصلاحيات الإدارة…'}</div></main>;
}
