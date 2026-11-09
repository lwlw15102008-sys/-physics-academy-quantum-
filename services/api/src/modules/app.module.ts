import { Global, Module } from "@nestjs/common";
import { APP_GUARD } from "@nestjs/core";
import { ThrottlerGuard, ThrottlerModule } from "@nestjs/throttler";
import { AuthGuard, RolesGuard } from "../auth/auth.guard";
import { APP_CONFIG, loadConfig } from "../config/env";
import { CatalogController } from "./catalog/catalog.controller";
import { HealthController } from "./health.controller";

@Global()
@Module({
  imports: [
    ThrottlerModule.forRootAsync({
      useFactory: () => {
        const c = loadConfig();
        return [{ ttl: c.throttleTtlMs, limit: c.throttleLimit }];
      },
    }),
  ],
  controllers: [HealthController, CatalogController],
  providers: [
    { provide: APP_CONFIG, useFactory: () => loadConfig() },
    // Order matters: rate limit -> authenticate -> authorize.
    { provide: APP_GUARD, useClass: ThrottlerGuard },
    { provide: APP_GUARD, useClass: AuthGuard },
    { provide: APP_GUARD, useClass: RolesGuard },
  ],
  exports: [APP_CONFIG],
})
export class AppModule {}
