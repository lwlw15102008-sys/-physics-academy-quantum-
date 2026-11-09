package com.example.physicsacademy;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;

import com.example.physicsacademy.databinding.FragmentProgressBinding;

public class ProgressFragment extends Fragment {
    private static final int[] LEVEL_IMAGES = {
            R.drawable.level_01_silver, R.drawable.level_02_gold, R.drawable.level_03_platinum, R.drawable.level_04_diamond, R.drawable.level_05_elite,
            R.drawable.level_06_star, R.drawable.level_07_hero, R.drawable.level_08_top, R.drawable.level_09_expert, R.drawable.level_10_innovator,
            R.drawable.level_11_sage, R.drawable.level_12_scholar, R.drawable.level_13_genius, R.drawable.level_14_master, R.drawable.level_15_legend};

    private FragmentProgressBinding binding;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        binding = FragmentProgressBinding.inflate(inflater, container, false);
        binding.levelsList.setLayoutManager(new GridLayoutManager(requireContext(), 3));
        binding.levelsList.setAdapter(new LevelAdapter(LEVEL_IMAGES, getResources().getStringArray(R.array.level_names)));
        return binding.getRoot();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
