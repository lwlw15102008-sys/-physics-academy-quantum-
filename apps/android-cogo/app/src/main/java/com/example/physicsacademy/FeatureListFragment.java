package com.example.physicsacademy;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;

import com.example.physicsacademy.databinding.FragmentFeatureListBinding;

import java.util.ArrayList;
import java.util.List;

/** Card list with cover images. Used for both the labs and the games tabs. */
public class FeatureListFragment extends Fragment {
    private static final String ARG_KIND = "kind";
    private static final int KIND_LABS = 0;
    private static final int KIND_GAMES = 1;

    private static final int[] LAB_IMAGES = {R.drawable.lab_physics, R.drawable.lab_chemistry, R.drawable.lab_biology, R.drawable.lab_mathematics, R.drawable.lab_geology};
    private static final int[] GAME_IMAGES = {R.drawable.game_daily_challenge, R.drawable.game_science_puzzle, R.drawable.game_physics_challenge,
            R.drawable.game_chemistry_challenge, R.drawable.game_biology_challenge, R.drawable.game_time_challenge, R.drawable.game_experiment_game};

    private FragmentFeatureListBinding binding;

    public static FeatureListFragment labs() {
        return create(KIND_LABS);
    }

    public static FeatureListFragment games() {
        return create(KIND_GAMES);
    }

    private static FeatureListFragment create(int kind) {
        FeatureListFragment fragment = new FeatureListFragment();
        Bundle args = new Bundle();
        args.putInt(ARG_KIND, kind);
        fragment.setArguments(args);
        return fragment;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        binding = FragmentFeatureListBinding.inflate(inflater, container, false);
        Bundle args = getArguments();
        boolean labs = args == null || args.getInt(ARG_KIND, KIND_LABS) == KIND_LABS;

        binding.listTitle.setText(labs ? R.string.labs_title : R.string.games_title);
        binding.listSubtitle.setText(labs ? R.string.labs_subtitle : R.string.games_subtitle);

        String[] titles = getResources().getStringArray(labs ? R.array.lab_titles : R.array.game_titles);
        String[] blurbs = getResources().getStringArray(labs ? R.array.lab_blurbs : R.array.game_blurbs);
        int[] images = labs ? LAB_IMAGES : GAME_IMAGES;

        List<FeatureItem> items = new ArrayList<>();
        for (int i = 0; i < titles.length && i < blurbs.length && i < images.length; i++) {
            items.add(new FeatureItem(titles[i], blurbs[i], images[i]));
        }

        binding.featureList.setLayoutManager(new LinearLayoutManager(requireContext()));
        binding.featureList.setAdapter(new FeatureAdapter(items,
                item -> Toast.makeText(requireContext(), getString(R.string.feature_pending, item.title), Toast.LENGTH_SHORT).show()));
        return binding.getRoot();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
