import { Controller, Get, Header, NotFoundException, Param } from "@nestjs/common";
import { IsString, Matches, MaxLength } from "class-validator";
import { Public } from "../../auth/decorators";

export class SlugParamDto {
  @IsString()
  @MaxLength(32)
  @Matches(/^[a-z][a-z-]*$/, { message: "slug must be lowercase letters and dashes" })
  slug!: string;
}

// Demo catalogue only. Replace with Prisma-backed queries once DATABASE_URL is configured.
export const demoSubjects = [
  { id: "physics", slug: "physics", title: "الفيزياء", description: "افهم قوانين الكون بالحساب والتجربة", sortOrder: 1 },
  { id: "chemistry", slug: "chemistry", title: "الكيمياء", description: "اكتشف المادة والتفاعلات", sortOrder: 2 },
  { id: "biology", slug: "biology", title: "الأحياء", description: "استكشف أسرار الحياة", sortOrder: 3 },
  { id: "mathematics", slug: "mathematics", title: "الرياضيات", description: "حوّل الأرقام إلى أفكار", sortOrder: 4 },
  { id: "geology", slug: "geology", title: "الجيولوجيا", description: "اقرأ تاريخ الأرض", sortOrder: 5 },
] as const;

@Controller("catalog")
export class CatalogController {
  @Public()
  @Get("subjects")
  @Header("Cache-Control", "public, max-age=60")
  getSubjects() {
    return { data: demoSubjects, source: "demo-seed", persistent: false };
  }

  @Public()
  @Get("subjects/:slug")
  @Header("Cache-Control", "public, max-age=60")
  getSubject(@Param() params: SlugParamDto) {
    const subject = demoSubjects.find((item) => item.slug === params.slug);
    if (!subject) throw new NotFoundException({ code: "SUBJECT_NOT_FOUND", message: "Subject not found" });
    return { data: subject, source: "demo-seed", persistent: false };
  }

  // Per-user data: requires authentication (global guard) and is never cached.
  @Get("learning-path")
  @Header("Cache-Control", "no-store")
  getLearningPath() {
    return {
      data: demoSubjects.map((s) => ({ subjectId: s.id, title: s.title, status: "CONTENT_PENDING", progress: 0 })),
      source: "demo-seed",
      persistent: false,
    };
  }
}
