package com.example.physicsacademy;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.fragment.app.Fragment;

import com.example.physicsacademy.databinding.FragmentHomeBinding;
import com.example.physicsacademy.databinding.ItemStatBinding;

public class HomeFragment extends Fragment {
    private FragmentHomeBinding binding;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        binding = FragmentHomeBinding.inflate(inflater, container, false);

        addStat(binding.statsRowOne, R.string.stat_time, R.string.stat_value_none, R.string.stat_time_hint);
        addStat(binding.statsRowOne, R.string.stat_goal, R.string.stat_value_unset, R.string.stat_goal_hint);
        addStat(binding.statsRowTwo, R.string.stat_achievements, R.string.stat_value_none, R.string.stat_achievements_hint);
        addStat(binding.statsRowTwo, R.string.stat_plan, R.string.stat_value_unplanned, R.string.stat_plan_hint);

        binding.startButton.setOnClickListener(v -> ((MainActivity) requireActivity()).openTab(R.id.nav_learn));
        return binding.getRoot();
    }

    private void addStat(LinearLayout row, @StringRes int label, @StringRes int value, @StringRes int hint) {
        ItemStatBinding stat = ItemStatBinding.inflate(getLayoutInflater(), row, false);
        stat.statLabel.setText(label);
        stat.statValue.setText(value);
        stat.statHint.setText(hint);
        row.addView(stat.getRoot());
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
