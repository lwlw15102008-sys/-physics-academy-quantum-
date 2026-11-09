package com.example.physicsacademy;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/** Local, offline catalogue. Replaced by real content storage in a later phase. */
public final class SubjectRepository {
    private static final List<Subject> ALL = Collections.unmodifiableList(Arrays.asList(
            new Subject("physics", R.string.subject_physics, R.string.subject_physics_sub, 0xFF3987FF, R.drawable.subject_physics),
            new Subject("chemistry", R.string.subject_chemistry, R.string.subject_chemistry_sub, 0xFF35D5E8, R.drawable.subject_chemistry),
            new Subject("biology", R.string.subject_biology, R.string.subject_biology_sub, 0xFF35D39A, R.drawable.subject_biology),
            new Subject("mathematics", R.string.subject_mathematics, R.string.subject_mathematics_sub, 0xFFA78BFA, R.drawable.subject_mathematics),
            new Subject("geology", R.string.subject_geology, R.string.subject_geology_sub, 0xFFFFBF69, R.drawable.subject_geology)
    ));

    private SubjectRepository() {}

    public static List<Subject> all() {
        return ALL;
    }
}
