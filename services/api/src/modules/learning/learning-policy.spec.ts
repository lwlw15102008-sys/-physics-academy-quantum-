import {
  areActivitiesUnlocked,
  evaluateLessonGate,
  getVideoCompletionPercent,
  isFinalExamPassed,
} from "./learning-policy";

describe("learning progression policy", () => {
  it("calculates video completion and caps it at 100%", () => {
    expect(getVideoCompletionPercent({ durationSeconds: 3600, watchedSeconds: 3240 })).toBe(90);
    expect(getVideoCompletionPercent({ durationSeconds: 30, watchedSeconds: 60 })).toBe(100);
  });

  it("rejects invalid video durations and watch times", () => {
    expect(() => getVideoCompletionPercent({ durationSeconds: 0, watchedSeconds: 0 })).toThrow(RangeError);
    expect(() => getVideoCompletionPercent({ durationSeconds: 10, watchedSeconds: -1 })).toThrow(RangeError);
  });

  it("keeps activities locked below 90% and unlocks at 90%", () => {
    expect(areActivitiesUnlocked({ durationSeconds: 100, watchedSeconds: 89 })).toBe(false);
    expect(areActivitiesUnlocked({ durationSeconds: 100, watchedSeconds: 90 })).toBe(true);
  });

  it("locks lessons until the previous lesson is passed", () => {
    const result = evaluateLessonGate({
      progress: { durationSeconds: 100, watchedSeconds: 100 },
      previousLessonPassed: false,
    });
    expect(result.status).toBe("LOCKED_PREVIOUS_LESSON");
  });

  it("allows video playback but not activities before the watch threshold", () => {
    const result = evaluateLessonGate({
      progress: { durationSeconds: 100, watchedSeconds: 89 },
      previousLessonPassed: true,
    });
    expect(result.status).toBe("IN_PROGRESS");
    expect(result.activitiesUnlocked).toBe(false);
  });

  it("unlocks activities at the configured threshold", () => {
    const result = evaluateLessonGate({
      progress: { durationSeconds: 100, watchedSeconds: 90 },
      previousLessonPassed: true,
    });
    expect(result.status).toBe("ACTIVITIES_UNLOCKED");
    expect(result.activitiesUnlocked).toBe(true);
  });

  it("gives an admin lock precedence over an admin unlock", () => {
    const result = evaluateLessonGate({
      progress: { durationSeconds: 100, watchedSeconds: 100 },
      previousLessonPassed: true,
      adminLocked: true,
      adminUnlocked: true,
    });
    expect(result.status).toBe("LOCKED_BY_ADMIN");
  });

  it("lets an explicit admin unlock bypass the previous-lesson gate", () => {
    const result = evaluateLessonGate({
      progress: { durationSeconds: 100, watchedSeconds: 0 },
      previousLessonPassed: false,
      adminUnlocked: true,
    });
    expect(result.status).toBe("ACTIVITIES_UNLOCKED");
  });

  it("requires at least 50 questions and at least 50% to pass by default", () => {
    expect(isFinalExamPassed({ questionCount: 49, correctAnswers: 49 })).toBe(false);
    expect(isFinalExamPassed({ questionCount: 50, correctAnswers: 24 })).toBe(false);
    expect(isFinalExamPassed({ questionCount: 50, correctAnswers: 25 })).toBe(true);
  });

  it("supports owner-configurable exam policy", () => {
    expect(isFinalExamPassed(
      { questionCount: 20, correctAnswers: 15 },
      { videoCompletionPercent: 95, finalExamMinQuestions: 20, finalExamPassPercent: 75 },
    )).toBe(true);
  });

  it("rejects impossible exam result counts", () => {
    expect(() => isFinalExamPassed({ questionCount: 10, correctAnswers: 11 })).toThrow(RangeError);
  });
});
