import { Controller, Get, Header } from "@nestjs/common";
import { Public } from "../auth/decorators";

@Controller("health")
export class HealthController {
  @Public()
  @Get()
  @Header("Cache-Control", "no-store")
  getHealth() {
    return { status: "ok", service: "physics-academy-api" };
  }
}
