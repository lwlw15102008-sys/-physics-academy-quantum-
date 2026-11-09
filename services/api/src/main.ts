import "reflect-metadata";
import { config as loadDotenv } from "dotenv";
import { ValidationPipe } from "@nestjs/common";
import { NestFactory } from "@nestjs/core";
import type { NestExpressApplication } from "@nestjs/platform-express";
import helmet from "helmet";
import { AllExceptionsFilter } from "./common/http-exception.filter";
import { loadConfig } from "./config/env";
import { AppModule } from "./modules/app.module";

async function bootstrap() {
  loadDotenv({ path: [".env", "../../.env"] });
  const config = loadConfig(); // throws on unsafe production configuration

  const app = await NestFactory.create<NestExpressApplication>(AppModule, { bodyParser: false });
  if (config.trustProxy) app.set("trust proxy", config.trustProxy);

  app.use(helmet());
  app.useBodyParser("json", { limit: "100kb" });
  app.useBodyParser("urlencoded", { limit: "100kb", extended: false });

  app.setGlobalPrefix("api/v1");
  app.enableCors({
    origin: config.corsOrigins, // explicit allow-list only, never reflected/wildcard
    methods: ["GET", "POST", "PATCH", "DELETE"],
    allowedHeaders: ["Authorization", "Content-Type", "X-Request-Id"],
    credentials: false, // bearer-token auth: no cookies, so no CSRF surface
    maxAge: 600,
  });
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, forbidUnknownValues: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  app.enableShutdownHooks();

  await app.listen(config.port, "0.0.0.0");
}
void bootstrap();
