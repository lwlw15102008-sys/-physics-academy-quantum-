package com.example.physicsacademy;

/** A card with a cover image (a lab or a game). Immutable. */
public final class FeatureItem {
    public final String title;
    public final String blurb;
    public final int imageRes;

    public FeatureItem(String title, String blurb, int imageRes) {
        this.title = title;
        this.blurb = blurb;
        this.imageRes = imageRes;
    }
}
