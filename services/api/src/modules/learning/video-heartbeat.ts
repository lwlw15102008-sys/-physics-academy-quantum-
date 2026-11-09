/**
 * Server-side playback heartbeat validation.
 *
 * A client may report its current media position, but cannot claim an arbitrary
 * watched duration. The server derives credited seconds from wall-clock time,
 * caps each heartbeat window, and rejects implausible seeking/speed changes.
 * Persist the returned state atomically per user+lesson in the API layer.
 */
export interface PlaybackState {
  lastPositionSeconds: number;
  creditedSeconds: number;
  lastHeartbeatAtMs: number;
  durationSeconds: number;
}

export interface HeartbeatInput {
  positionSeconds: number;
  durationSeconds: number;
  nowMs: number;
}

export interface HeartbeatResult {
  accepted: boolean;
  reason?: "INVALID_POSITION" | "DURATION_MISMATCH" | "HEARTBEAT_TOO_SOON" | "HEARTBEAT_EXPIRED" | "SEEK_DETECTED";
  state: PlaybackState;
  creditedDeltaSeconds: number;
  completionPercent: number;
}

const MAX_HEARTBEAT_GAP_MS = 30_000;
const MIN_HEARTBEAT_GAP_MS = 2_000;
const MAX_CREDIT_PER_HEARTBEAT_SECONDS = 15;
const POSITION_TOLERANCE_SECONDS = 3;

export function applyPlaybackHeartbeat(
  previous: PlaybackState | null,
  input: HeartbeatInput,
): HeartbeatResult {
  const empty: PlaybackState = {
    lastPositionSeconds: 0,
    creditedSeconds: 0,
    lastHeartbeatAtMs: input.nowMs,
    durationSeconds: input.durationSeconds,
  };
  const reject = (reason: NonNullable<HeartbeatResult["reason"]>, state = previous ?? empty): HeartbeatResult => ({
    accepted: false, reason, state, creditedDeltaSeconds: 0,
    completionPercent: state.durationSeconds > 0
      ? Math.min(100, Math.floor(state.creditedSeconds / state.durationSeconds * 100)) : 0,
  });

  if (!Number.isFinite(input.positionSeconds) || !Number.isFinite(input.durationSeconds) ||
      !Number.isFinite(input.nowMs) || input.durationSeconds <= 0 ||
      input.positionSeconds < 0 || input.positionSeconds > input.durationSeconds + 1) {
    return reject("INVALID_POSITION");
  }

  if (!previous) {
    const state = { ...empty, lastPositionSeconds: Math.min(input.positionSeconds, input.durationSeconds) };
    return { accepted: true, state, creditedDeltaSeconds: 0, completionPercent: 0 };
  }

  if (Math.abs(previous.durationSeconds - input.durationSeconds) > 1) return reject("DURATION_MISMATCH");
  const elapsedMs = input.nowMs - previous.lastHeartbeatAtMs;
  if (elapsedMs < MIN_HEARTBEAT_GAP_MS) return reject("HEARTBEAT_TOO_SOON");
  if (elapsedMs > MAX_HEARTBEAT_GAP_MS) return reject("HEARTBEAT_EXPIRED");

  const elapsedSeconds = elapsedMs / 1000;
  const positionDelta = input.positionSeconds - previous.lastPositionSeconds;
  if (positionDelta < -POSITION_TOLERANCE_SECONDS ||
      positionDelta > elapsedSeconds + POSITION_TOLERANCE_SECONDS) return reject("SEEK_DETECTED");

  const creditedDeltaSeconds = Math.min(
    MAX_CREDIT_PER_HEARTBEAT_SECONDS,
    Math.max(0, Math.floor(Math.min(elapsedSeconds, Math.max(0, positionDelta)))),
  );
  const state: PlaybackState = {
    lastPositionSeconds: Math.min(input.positionSeconds, input.durationSeconds),
    creditedSeconds: Math.min(input.durationSeconds, previous.creditedSeconds + creditedDeltaSeconds),
    lastHeartbeatAtMs: input.nowMs,
    durationSeconds: previous.durationSeconds,
  };
  return {
    accepted: true, state, creditedDeltaSeconds,
    completionPercent: Math.min(100, Math.floor(state.creditedSeconds / state.durationSeconds * 100)),
  };
}
