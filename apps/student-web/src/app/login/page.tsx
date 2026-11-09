'use client';

import { useState } from 'react';
import { Atom, ShieldCheck } from 'lucide-react';
import { getSupabase } from '@/lib/supabase';

export default function LoginPage() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const message = typeof window === 'undefined' ? null : new URLSearchParams(window.location.search).get('message');

  async function continueWithGoogle() {
    setBusy(true); setError('');
    try {
      const supabase = getSupabase();
      const { error: authError } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: { redirectTo: `${window.location.origin}/auth/callback`, queryParams: { prompt: 'select_account' } },
      });
      if (authError) throw authError;
    } catch (e) {
      setError(e instanceof Error ? e.message : 'تعذر بدء تسجيل الدخول. حاول مرة أخرى.');
      setBusy(false);
    }
  }

  return (
    <main dir="rtl" className="min-h-screen grid place-items-center p-5 bg-[#080D1A] text-white">
      <section className="w-full max-w-md rounded-3xl border border-cyan-300/15 bg-[#111B30] p-8 text-center shadow-2xl">
        <div className="mx-auto mb-5 grid h-16 w-16 place-items-center rounded-2xl bg-cyan-300/10 text-cyan-300"><Atom size={36}/></div>
        <p className="text-xs font-bold tracking-[.2em] text-cyan-300">PHYSICS ACADEMY</p>
        <h1 className="mt-3 text-2xl font-black">مرحباً بك في عالمك العلمي</h1>
        <p className="mt-3 text-sm leading-7 text-slate-300">سجّل دخولك بحساب Google للمتابعة إلى رحلتك التعليمية.</p>
        <button onClick={continueWithGoogle} disabled={busy} className="mt-7 flex w-full items-center justify-center gap-3 rounded-xl bg-white px-5 py-4 font-bold text-slate-800 transition hover:bg-slate-100 disabled:opacity-60">
          <svg viewBox="0 0 48 48" aria-hidden="true" className="h-5 w-5"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5Z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.73 7.18l7.27 5.64c4.24-3.91 6.7-9.68 6.7-17.29Z"/><path fill="#FBBC05" d="M10.54 28.59A14.4 14.4 0 0 1 9.75 24c0-1.59.27-3.13.76-4.59l-7.98-6.2A23.9 23.9 0 0 0 0 24c0 3.87.93 7.53 2.56 10.78l7.98-6.19Z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.9-5.8l-7.27-5.64c-2.02 1.35-4.6 2.15-8.63 2.15-6.26 0-11.57-4.22-13.46-9.91l-7.98 6.19C6.51 43.62 14.62 48 24 48Z"/></svg>
          {busy ? 'جارٍ تحويلك إلى Google…' : 'المتابعة باستخدام Google'}
        </button>
        {error && <p role="alert" className="mt-4 text-sm text-rose-300">{error}</p>}
        {message && <p className="mt-4 text-sm text-amber-200">{message}</p>}
        <p className="mt-6 flex items-center justify-center gap-2 text-xs text-slate-400"><ShieldCheck size={15}/> تسجيل آمن — لا يوجد إنشاء حساب يدوي أو كلمة مرور.</p>
      </section>
    </main>
  );
}
