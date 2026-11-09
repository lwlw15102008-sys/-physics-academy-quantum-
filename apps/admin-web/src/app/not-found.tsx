import Link from "next/link";

export default function NotFound() {
  return (
    <main className="min-h-screen grid place-items-center p-6 text-center">
      <div className="panel p-8 max-w-md">
        <h1 className="text-xl font-black">الصفحة غير موجودة</h1>
        <Link href="/" className="inline-block mt-5 rounded-xl bg-blue-500 px-4 py-2 text-sm">العودة للوحة</Link>
      </div>
    </main>
  );
}
