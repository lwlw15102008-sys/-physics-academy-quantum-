import { ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus, Logger } from "@nestjs/common";
import { randomUUID } from "node:crypto";
import type { Request, Response } from "express";

const CODE_BY_STATUS: Record<number, string> = {
  400: "BAD_REQUEST",
  401: "UNAUTHORIZED",
  403: "FORBIDDEN",
  404: "NOT_FOUND",
  413: "PAYLOAD_TOO_LARGE",
  429: "RATE_LIMITED",
  503: "UNAVAILABLE",
};

const REQUEST_ID = /^[A-Za-z0-9-]{8,64}$/;

export function resolveRequestId(incoming: unknown): string {
  return typeof incoming === "string" && REQUEST_ID.test(incoming) ? incoming : randomUUID();
}

/** One error shape for every failure: { error: { code, message, requestId } }. Internals never leak. */
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger("Http");

  catch(exception: unknown, host: ArgumentsHost): void {
    const http = host.switchToHttp();
    const req = http.getRequest<Request>();
    const res = http.getResponse<Response>();
    const requestId = resolveRequestId(req.headers["x-request-id"]);

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let code = "INTERNAL_ERROR";
    let message = "Internal server error";

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      code = CODE_BY_STATUS[status] ?? "ERROR";
      const body = exception.getResponse();
      if (typeof body === "string") {
        message = body;
      } else if (body && typeof body === "object") {
        const b = body as { code?: unknown; message?: unknown };
        if (typeof b.code === "string") code = b.code;
        if (Array.isArray(b.message)) message = b.message.map(String).join("; ");
        else if (typeof b.message === "string") message = b.message;
      }
    }

    if (status >= 500) {
      this.logger.error(`[${requestId}] ${req.method} ${req.url} -> ${status}`, exception instanceof Error ? exception.stack : String(exception));
      message = status === 503 && code !== "INTERNAL_ERROR" ? message : "Internal server error";
    }

    res.setHeader("x-request-id", requestId);
    res.setHeader("Cache-Control", "no-store");
    res.status(status).json({ error: { code, message, requestId } });
  }
}
