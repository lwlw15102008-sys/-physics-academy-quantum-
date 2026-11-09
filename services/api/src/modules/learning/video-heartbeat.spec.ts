import { applyPlaybackHeartbeat, PlaybackState } from "./video-heartbeat";

describe("applyPlaybackHeartbeat", () => {
  const initial: PlaybackState = {
    lastPositionSeconds: 0, creditedSeconds: 0, lastHeartbeatAtMs: 1_000,
    durationSeconds: 100,
  };

  it("starts a playback session without granting watch credit", () => {
    const result = applyPlaybackHeartbeat(null, { positionSeconds: 0, durationSeconds: 100, nowMs: 1_000 });
    expect(result.accepted).toBe(true);
    expect(result.creditedDeltaSeconds).toBe(0);
  });

  it("credits only elapsed playback time", () => {
    const result = applyPlaybackHeartbeat(initial, { positionSeconds: 10, durationSeconds: 100, nowMs: 11_000 });
    expect(result.creditedDeltaSeconds).toBe(10);
    expect(result.state.creditedSeconds).toBe(10);
  });

  it("caps credit per heartbeat", () => {
    const result = applyPlaybackHeartbeat(initial, { positionSeconds: 30, durationSeconds: 100, nowMs: 31_000 });
    expect(result.creditedDeltaSeconds).toBe(15);
  });

  it("rejects seeking forward", () => {
    const result = applyPlaybackHeartbeat(initial, { positionSeconds: 60, durationSeconds: 100, nowMs: 11_000 });
    expect(result).toMatchObject({ accepted: false, reason: "SEEK_DETECTED" });
  });

  it("rejects backward seeking", () => {
    const state = { ...initial, lastPositionSeconds: 20 };
    const result = applyPlaybackHeartbeat(state, { positionSeconds: 0, durationSeconds: 100, nowMs: 11_000 });
    expect(result.reason).toBe("SEEK_DETECTED");
  });

  it("rejects heartbeat spam", () => {
    const result = applyPlaybackHeartbeat(initial, { positionSeconds: 1, durationSeconds: 100, nowMs: 2_000 });
    expect(result.reason).toBe("HEARTBEAT_TOO_SOON");
  });

  it("rejects stale heartbeat gaps", () => {
    const result = applyPlaybackHeartbeat(initial, { positionSeconds: 20, durationSeconds: 100, nowMs: 40_000 });
    expect(result.reason).toBe("HEARTBEAT_EXPIRED");
  });

  it("rejects media duration changes", () => {
    const result = applyPlaybackHeartbeat(initial, { positionSeconds: 10, durationSeconds: 200, nowMs: 11_000 });
    expect(result.reason).toBe("DURATION_MISMATCH");
  });

  it("never credits more than media duration", () => {
    const state = { ...initial, creditedSeconds: 98, lastPositionSeconds: 98 };
    const result = applyPlaybackHeartbeat(state, { positionSeconds: 100, durationSeconds: 100, nowMs: 11_000 });
    expect(result.state.creditedSeconds).toBeLessThanOrEqual(100);
  });
});
