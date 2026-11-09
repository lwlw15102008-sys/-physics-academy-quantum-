// Copies the shipped subset of PHYSICS_ACADEMY_ASSETS into <app>/public/assets (generated, git-ignored).
// Usage: node scripts/sync-assets.mjs <student-web|admin-web>
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SRC = path.join(root, "PHYSICS_ACADEMY_ASSETS");
const app = process.argv[2];

// { from: folder under SRC, to: folder under public/assets, ext: allowed extensions, only: optional file-name whitelist }
const PLANS = {
  "student-web": [
    { from: "03_SUBJECTS", to: "subjects", ext: [".webp"] },
    { from: "04_LABORATORIES/backgrounds", to: "labs", ext: [".webp"] },
    { from: "05_GAMES/covers", to: "games", ext: [".webp"] },
    { from: "06_REWARDS/levels", to: "levels", ext: [".png"] },
    { from: "06_REWARDS/trophies", to: "rewards", ext: [".png"] },
    { from: "02_AI_TEACHER/characters", to: "teacher", ext: [".png"] },
    { from: "02_AI_TEACHER/expressions", to: "teacher", ext: [".png"] },
    { from: "10_SUBSCRIPTIONS", to: "plans", ext: [".png"] },
  ],
  "admin-web": [
    { from: "11_WEBSITE", to: "bg", ext: [".webp"], only: ["admin_dashboard_bg.webp"] },
    { from: "01_BRANDING/backgrounds", to: "brand", ext: [".webp"], only: ["auth_background.webp"] },
  ],
};

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]));
}

const plan = PLANS[app];
if (!plan) {
  console.error(`sync-assets: unknown app "${app}" (expected ${Object.keys(PLANS).join(" | ")})`);
  process.exit(1);
}
if (!fs.existsSync(SRC)) {
  console.warn("sync-assets: PHYSICS_ACADEMY_ASSETS not found, skipping (existing public/assets, if any, is kept).");
  process.exit(0);
}

const dest = path.join(root, "apps", app, "public", "assets");
fs.rmSync(dest, { recursive: true, force: true });
let count = 0;
for (const { from, to, ext, only } of plan) {
  const base = path.join(SRC, from);
  if (!fs.existsSync(base)) continue;
  for (const file of walk(base)) {
    const name = path.basename(file);
    if (!ext.includes(path.extname(name).toLowerCase())) continue;
    if (only && !only.includes(name)) continue;
    const out = path.join(dest, to, name);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.copyFileSync(file, out);
    count++;
  }
}
console.log(`sync-assets: ${count} files -> apps/${app}/public/assets`);
