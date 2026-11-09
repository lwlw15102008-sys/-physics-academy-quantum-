'use client';

import { useState } from 'react';
import { Lock } from 'lucide-react';
import { createClient } from '@supabase/supabase-js';

export default function LoginPage() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  async function signIn() {
    setBusy(true); setError('');
    try {
      const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
      const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
      if (!url || !key) throw new Error('إعدادات Google / Supabase غير مكتملة.');
      const supabase = createClient(url, key, { auth: { flowType: 'pkce', persistSession: true, detectSessionInUrl: false } });
      const { error: authError } = await supabase.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: `${window.location.origin}/auth/callback`, queryParams: { prompt: 'select_account' } } });
      if (authError) throw authError;
    } catch (e) { setError(e instanceof Error ? e.message : 'تعذر بدء تسجيل الدخول.'); setBusy(false); }
  }
  return (
    <main className="relative min-h-screen grid place-items-center p-6 overflow-hidden">
      <img src="/assets/brand/auth_background.webp" alt="" className="absolute inset-0 w-full h-full object-cover opacity-70" />
      <div className="panel relative p-8 max-w-md w-full text-center">
        <Lock className="mx-auto text-cyan-300" aria-hidden />
        <h1 className="text-xl font-black mt-4">دخول المالك والمدرس</h1>
        <p className="text-sm muted leading-7 mt-3">الدخول باستخدام حساب Google المعتمد فقط. يجب أن يكون الحساب مُنح صلاحية الإدارة مسبقاً.</p>
        <button onClick={signIn} disabled={busy} className="mt-6 w-full rounded-xl bg-white px-5 py-4 font-bold text-slate-900 disabled:opacity-60">{busy ? 'جارٍ التحويل إلى Google…' : 'المتابعة باستخدام Google'}</button>
        {error && <p role="alert" className="mt-4 text-sm text-rose-300">{error}</p>}
        <p className="mt-5 text-xs muted">لا يوجد إنشاء حساب يدوي أو دخول بكلمة مرور.</p>
      </div>
    </main>
  );
}
