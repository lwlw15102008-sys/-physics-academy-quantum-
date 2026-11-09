# Build log — v0.4.2

## Added
- Playback heartbeat validation policy (`services/api/src/modules/learning/video-heartbeat.ts`).
- Nine unit tests for normal playback, credit caps, seeking, heartbeat spam, stale intervals, duration mismatch, and duration bounds.
- Updated implementation status and package version.

## Validation
- TypeScript compiler validation for the new domain module.
- Runtime checks are recorded below after execution.

## Not yet complete
- No authenticated playback endpoint yet.
- No database persistence for heartbeat state yet.
- No media-provider signed playback verification.
- Therefore this addition is not, by itself, a production anti-cheat system.
