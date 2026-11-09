# Prompts لتوليد ما ينقص بأداة صور / 3D بالذكاء الاصطناعي

الأصول المولّدة برمجياً (انظر `ASSET_MANIFEST.md`) هي نسخة تشغيلية بهوية موحّدة. إن أردت جودة رندر سينمائي أو شخصيات 3D، استخدم هذه الأوامر. **تحقق من ترخيص الاستخدام التجاري لكل أداة قبل النشر**، واحتفظ بنفس أسماء الملفات ليحلّ الناتج محل الحالي دون تعديل الكود.

## الهوية البصرية المشتركة (ألصقها في بداية كل أمر)
> Futuristic educational science universe, deep navy background (#080D1A), electric blue (#3987FF), cyan (#35D5E8) and violet (#8957FF) accents, soft neon glow, clean premium 3D render, rounded forms, no text, no watermark, consistent lighting from top-left.

## المدرس الذكي (02_AI_TEACHER) — شخصية واحدة ثابتة
> Friendly AI science teacher mascot, young adult, warm smile, modern smart-casual outfit, holographic accents, 3D character render, transparent background, 1024x1024. **Same character in every image**; only the expression/pose changes: [happy | explaining with open hand | thinking with hand on chin | pointing at a board | congratulating with raised arms | guiding with extended hand | listening attentively].
نصيحة: ولّد الصورة الأساسية أولاً ثم استخدمها كمرجع (character reference / image-to-image) لباقي التعبيرات.

## شارات المستويات (06_REWARDS/levels) — 15 ملفاً 512×512 شفاف
> Premium 3D game rank badge, level {N} "{name}", {material/colour}, unique silhouette different from the previous level, high detail that stays readable at 64px, transparent background.
المواد/الألوان بالترتيب: فضي، ذهبي، بلاتيني، ماسي، تركوازي، نجم كهرماني، برتقالي-أحمر، وردي، بنفسجي، نيلي، أخضر، قرمزي، أرجواني كهربائي، ذهبي وردي، ذهبي ناري متوهّج.

## الكؤوس والميداليات (06_REWARDS/trophies, medals)
> 3D achievement trophy, rank {1-5}, {gold|silver|bronze|blue|purple} metal, polished, centred, transparent background, 512x512.

## أدوات المختبر (04_LABORATORIES) — كل أداة ملف منفصل بخلفية شفافة
> Isometric 3D {microscope | test tube rack with colourful liquids | beaker, flask and graduated cylinder | resistor, LED and switch | AA batteries with wires | animal cell cross-section | DNA double helix}, glossy glass and metal, transparent background, 512x512.

## نموذج جسم الإنسان (human_body_model.glb)
لا يُولَّد بالكود. اطلب نموذج تشريح مرخّصاً (GLB) أو ولّده بأداة image-to-3D ثم نظّف الشبكة، وضعه في `04_LABORATORIES/3d_models/`. أبقِ حجمه أقل من ~5MB للموبايل.

## خلفيات الصفحات (1920×1080 WebP)
> Wide cinematic background, {topic}, dark navy with soft nebula glow, large calm empty area on the left for UI text, 16:9.
