import type { SubjectSlug } from "@/lib/subjects";

// Files are copied from PHYSICS_ACADEMY_ASSETS into public/assets by scripts/sync-assets.mjs.
const FILE_NAME: Record<SubjectSlug, string> = { physics: "physics", chemistry: "chemistry", biology: "biology", mathematics: "math", geology: "geology" };

export const subjectImage = (slug: SubjectSlug) => `/assets/subjects/${FILE_NAME[slug]}_subject.webp`;
export const labImage = (slug: SubjectSlug) => `/assets/labs/${FILE_NAME[slug]}_lab_bg.webp`;

export const LABS: { slug: SubjectSlug; title: string; blurb: string }[] = [
  { slug: "physics", title: "مختبر الفيزياء", blurb: "حركة، قوى، دوائر كهربائية وموجات" },
  { slug: "chemistry", title: "مختبر الكيمياء", blurb: "تفاعلات ومحاليل وتجارب آمنة" },
  { slug: "biology", title: "مختبر الأحياء", blurb: "خلايا، مجهر، وراثة وDNA" },
  { slug: "mathematics", title: "مختبر الرياضيات", blurb: "دوال ورسوم وأشكال هندسية" },
  { slug: "geology", title: "مختبر الجيولوجيا", blurb: "طبقات الأرض والصخور والبراكين" },
];

export const GAMES: { file: string; title: string; blurb: string }[] = [
  { file: "daily_challenge", title: "التحدي اليومي", blurb: "سؤال جديد كل يوم وحافظ على سلسلتك" },
  { file: "science_puzzle", title: "ألغاز علمية", blurb: "رتّب المفاهيم وحُلّ الألغاز" },
  { file: "physics_challenge", title: "تحدي الفيزياء", blurb: "مسائل سريعة في قوانين الحركة" },
  { file: "chemistry_challenge", title: "تحدي الكيمياء", blurb: "عناصر ومركبات وتفاعلات" },
  { file: "biology_challenge", title: "تحدي الأحياء", blurb: "أجهزة الجسم والخلية" },
  { file: "time_challenge", title: "تحدي الوقت", blurb: "أجب قبل انتهاء العدّاد" },
  { file: "experiment_game", title: "لعبة التجارب", blurb: "نفّذ تجربة وشاهد النتيجة" },
];
export const gameImage = (file: string) => `/assets/games/${file}.webp`;

// Level names follow the asset brief (15 levels). XP thresholds live in database/seed/levels.json.
export const LEVELS: { n: number; slug: string; title: string }[] = [
  { n: 1, slug: "silver", title: "فضي" }, { n: 2, slug: "gold", title: "ذهبي" }, { n: 3, slug: "platinum", title: "بلاتيني" },
  { n: 4, slug: "diamond", title: "ماسي" }, { n: 5, slug: "elite", title: "متميز" }, { n: 6, slug: "star", title: "النجم" },
  { n: 7, slug: "hero", title: "البطل" }, { n: 8, slug: "top", title: "المتفوق" }, { n: 9, slug: "expert", title: "الخبير" },
  { n: 10, slug: "innovator", title: "المبتكر" }, { n: 11, slug: "sage", title: "الحكيم" }, { n: 12, slug: "scholar", title: "العلّامة" },
  { n: 13, slug: "genius", title: "النابغة" }, { n: 14, slug: "master", title: "الأستاذ" }, { n: 15, slug: "legend", title: "سيد المنهج" },
];
export const levelImage = (n: number, slug: string) => `/assets/levels/level_${String(n).padStart(2, "0")}_${slug}.png`;

export const TEACHER_IMAGE = "/assets/teacher/teacher_main.png";
