package com.example.physicsacademy;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.physicsacademy.databinding.ItemSubjectBinding;

import java.util.List;

public class SubjectAdapter extends RecyclerView.Adapter<SubjectAdapter.Holder> {

    public interface OnSubjectClick {
        void onSubjectClick(Subject subject);
    }

    private final List<Subject> items;
    private final OnSubjectClick listener;

    public SubjectAdapter(List<Subject> items, OnSubjectClick listener) {
        this.items = items;
        this.listener = listener;
    }

    @NonNull
    @Override
    public Holder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        ItemSubjectBinding b = ItemSubjectBinding.inflate(LayoutInflater.from(parent.getContext()), parent, false);
        return new Holder(b);
    }

    @Override
    public void onBindViewHolder(@NonNull Holder holder, int position) {
        Subject subject = items.get(position);
        ItemSubjectBinding b = holder.binding;
        b.subjectTitle.setText(subject.titleRes);
        b.subjectTitle.setTextColor(subject.color);
        b.subjectSubtitle.setText(subject.subtitleRes);
        b.subjectImage.setImageResource(subject.imageRes);
        b.getRoot().setOnClickListener(v -> listener.onSubjectClick(subject));
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    static class Holder extends RecyclerView.ViewHolder {
        final ItemSubjectBinding binding;

        Holder(ItemSubjectBinding binding) {
            super(binding.getRoot());
            this.binding = binding;
        }
    }
}
