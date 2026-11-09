import type { Metadata, Viewport } from "next";
import { Cairo } from "next/font/google";
import "@physics-academy/design-tokens/tokens.css";
import "./globals.css";

const cairo = Cairo({ subsets: ["arabic", "latin"], weight: ["400", "500", "600", "700", "800", "900"], display: "swap", variable: "--font-cairo" });

export const metadata: Metadata = {
  title: "PHYSICS ACADEMY | Quantum Learning Universe",
  description: "عالمك التعليمي الذكي — تعلّم، استكشف، وتقدّم",
};
export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#080D1A" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ar" dir="rtl" className={cairo.variable}>
      <body>{children}</body>
    </html>
  );
}
