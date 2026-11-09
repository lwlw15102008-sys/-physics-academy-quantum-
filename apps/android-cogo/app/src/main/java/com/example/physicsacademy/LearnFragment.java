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

import com.example.physicsacademy.databinding.FragmentLearnBinding;

public class LearnFragment extends Fragment {
    private FragmentLearnBinding binding;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        binding = FragmentLearnBinding.inflate(inflater, container, false);
        binding.subjectsList.setLayoutManager(new LinearLayoutManager(requireContext()));
        binding.subjectsList.setAdapter(new SubjectAdapter(SubjectRepository.all(), subject -> {
            String title = getString(subject.titleRes);
            Toast.makeText(requireContext(), getString(R.string.subject_pending, title), Toast.LENGTH_SHORT).show();
        }));
        return binding.getRoot();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
