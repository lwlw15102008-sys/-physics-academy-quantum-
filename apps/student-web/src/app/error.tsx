"use client";

// Shows a generic message only: error details must never be rendered to the user.
export default function GlobalError({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <main className="min-h-screen grid place-items-center p-6 text-center">
      <div className="panel p-8 max-w-md" role="alert">
        <h1 className="text-2xl font-black">حدث خطأ غير متوقع</h1>
        <p className="muted text-sm mt-3">يرجى المحاولة مرة أخرى.</p>
        <button onClick={reset} className="mt-5 rounded-xl bg-gradient-to-l from-blue-500 to-cyan-400 text-slate-950 font-extrabold px-5 py-3 text-sm">إعادة المحاولة</button>
      </div>
    </main>
  );
}
