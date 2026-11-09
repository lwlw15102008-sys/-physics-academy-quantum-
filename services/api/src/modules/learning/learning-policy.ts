/**
 * Learning progression rules.
 *
 * Inputs to this module must come from trusted server-side records. In particular,
 * watchedSeconds must be accumulated from validated playback heartbeats, never
 * accepted as a final value from the student client.
 */
export interface LearningPolicy {
  videoCompletionPercent: number;
  finalExamMinQuestions: number;
  finalExamPassPercent: number;
}

export const DEFAULT_LEARNING_POLICY: Readonly<LearningPolicy> = Object.freeze({
  videoCompletionPercent: 90,
  finalExamMinQuestions: 50,
  finalExamPassPercent: 50,
});

export interface VideoProgress {
  durationSeconds: number;
  watchedSeconds: number;
}

export interface FinalExamResult {
  questionCount: number;
  correctAnswers: number;
}

export type LessonGate =
  | { status: "LOCKED_BY_ADMIN"; canWatch: false; activitiesUnlocked: false; reason: string }
  | { status: "LOCKED_PREVIOUS_LESSON"; canWatch: false; activitiesUnlocked: false; reason: string }
  | { status: "IN_PROGRESS"; canWatch: true; activitiesUnlocked: false; videoCompletionPercent: number; requiredPercent: number }
  | { status: "ACTIVITIES_UNLOCKED"; canWatch: true; activitiesUnlocked: true; videoCompletionPercent: number; requiredPercent: number };

function assertPercent(value: number, name: string): void {
  if (!Number.isFinite(value) || value < 0 || value > 100) {
    throw new RangeError(`${name} must be between 0 and 100`);
  }
}

export function getVideoCompletionPercent(progress: VideoProgress): number {
  if (!Number.isFinite(progress.durationSeconds) || progress.durationSeconds <= 0) {
    throw new RangeError("durationSeconds must be greater than zero");
  }
  if (!Number.isFinite(progress.watchedSeconds) || progress.watchedSeconds < 0) {
    throw new RangeError("watchedSeconds must be zero or greater");
  }
  return Math.min(100, Math.floor((progress.watchedSeconds / progress.durationSeconds) * 100));
}

export function areActivitiesUnlocked(
  progress: VideoProgress,
  policy: LearningPolicy = DEFAULT_LEARNING_POLICY,
): boolean {
  assertPercent(policy.videoCompletionPercent, "videoCompletionPercent");
  return getVideoCompletionPercent(progress) >= policy.videoCompletionPercent;
}

/** Admin lock takes precedence; explicit admin unlock bypasses lesson prerequisites. */
export function evaluateLessonGate(input: {
  progress: VideoProgress;
  previousLessonPassed: boolean;
  adminLocked?: boolean;
  adminUnlocked?: boolean;
  policy?: LearningPolicy;
}): LessonGate {
  const policy = input.policy ?? DEFAULT_LEARNING_POLICY;
  assertPercent(policy.videoCompletionPercent, "videoCompletionPercent");

  if (input.adminLocked) {
    return { status: "LOCKED_BY_ADMIN", canWatch: false, activitiesUnlocked: false, reason: "تم قفل الدرس بواسطة الإدارة" };
  }
  if (input.adminUnlocked) {
    return {
      status: "ACTIVITIES_UNLOCKED",
      canWatch: true,
      activitiesUnlocked: true,
      videoCompletionPercent: getVideoCompletionPercent(input.progress),
      requiredPercent: policy.videoCompletionPercent,
    };
  }
  if (!input.previousLessonPassed) {
    return { status: "LOCKED_PREVIOUS_LESSON", canWatch: false, activitiesUnlocked: false, reason: "يجب اجتياز امتحان الدرس السابق أولاً" };
  }

  const percent = getVideoCompletionPercent(input.progress);
  if (percent < policy.videoCompletionPercent) {
    return { status: "IN_PROGRESS", canWatch: true, activitiesUnlocked: false, videoCompletionPercent: percent, requiredPercent: policy.videoCompletionPercent };
  }
  return { status: "ACTIVITIES_UNLOCKED", canWatch: true, activitiesUnlocked: true, videoCompletionPercent: percent, requiredPercent: policy.videoCompletionPercent };
}

export function isFinalExamPassed(
  result: FinalExamResult,
  policy: LearningPolicy = DEFAULT_LEARNING_POLICY,
): boolean {
  if (!Number.isInteger(policy.finalExamMinQuestions) || policy.finalExamMinQuestions < 1) {
    throw new RangeError("finalExamMinQuestions must be a positive integer");
  }
  assertPercent(policy.finalExamPassPercent, "finalExamPassPercent");
  if (!Number.isInteger(result.questionCount) || result.questionCount < 0 ||
      !Number.isInteger(result.correctAnswers) || result.correctAnswers < 0 ||
      result.correctAnswers > result.questionCount) {
    throw new RangeError("exam result contains invalid question counts");
  }
  if (result.questionCount < policy.finalExamMinQuestions) return false;
  return (result.correctAnswers / result.questionCount) * 100 >= policy.finalExamPassPercent;
}
