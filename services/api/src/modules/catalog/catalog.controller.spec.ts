import { NotFoundException } from "@nestjs/common";
import { validate } from "class-validator";
import { CatalogController, SlugParamDto } from "./catalog.controller";

describe("CatalogController", () => {
  const controller = new CatalogController();

  it("lists the five demo subjects and marks them non-persistent", () => {
    const res = controller.getSubjects();
    expect(res.data.length).toBe(5);
    expect(res.persistent).toBe(false);
  });
  it("returns 404 (not 200) for an unknown subject", () => {
    const dto = Object.assign(new SlugParamDto(), { slug: "astrology" });
    expect(() => controller.getSubject(dto)).toThrow(NotFoundException);
  });
  it("rejects malformed slugs at validation time", async () => {
    for (const slug of ["Physics", "../etc", "a b", "x".repeat(40), "1abc"]) {
      const errors = await validate(Object.assign(new SlugParamDto(), { slug }));
      expect(errors.length > 0).toBe(true);
    }
    expect((await validate(Object.assign(new SlugParamDto(), { slug: "physics" }))).length).toBe(0);
  });
});
