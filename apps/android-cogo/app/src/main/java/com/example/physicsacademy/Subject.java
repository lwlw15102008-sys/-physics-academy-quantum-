package com.example.physicsacademy;

/** A school subject shown in the catalogue. Immutable. */
public final class Subject {
    public final String slug;
    public final int titleRes;
    public final int subtitleRes;
    public final int color;
    public final int imageRes;

    public Subject(String slug, int titleRes, int subtitleRes, int color, int imageRes) {
        this.slug = slug;
        this.titleRes = titleRes;
        this.subtitleRes = subtitleRes;
        this.color = color;
        this.imageRes = imageRes;
    }
}
