import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        dim: "var(--qa-dim)",
        quantum: { bg: "var(--qa-bg)", card: "var(--qa-card)", blue: "var(--qa-blue)", cyan: "var(--qa-cyan)", purple: "var(--qa-purple)" },
      },
    },
  },
  plugins: [],
};
export default config;
