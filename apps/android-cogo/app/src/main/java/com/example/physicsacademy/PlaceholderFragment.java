package com.example.physicsacademy;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.fragment.app.Fragment;

import com.example.physicsacademy.databinding.FragmentPlaceholderBinding;

/** Temporary screen for sections that are not built yet (labs, games, progress). */
public class PlaceholderFragment extends Fragment {
    private static final String ARG_TITLE = "title";

    private FragmentPlaceholderBinding binding;

    public static PlaceholderFragment newInstance(@StringRes int titleRes) {
        PlaceholderFragment fragment = new PlaceholderFragment();
        Bundle args = new Bundle();
        args.putInt(ARG_TITLE, titleRes);
        fragment.setArguments(args);
        return fragment;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        binding = FragmentPlaceholderBinding.inflate(inflater, container, false);
        Bundle args = getArguments();
        int titleRes = args != null ? args.getInt(ARG_TITLE, R.string.app_name) : R.string.app_name;
        binding.placeholderTitle.setText(titleRes);
        binding.placeholderMessage.setText(R.string.coming_soon);
        return binding.getRoot();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
