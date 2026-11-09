package com.example.physicsacademy;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.physicsacademy.databinding.ItemFeatureBinding;

import java.util.List;

public class FeatureAdapter extends RecyclerView.Adapter<FeatureAdapter.Holder> {

    public interface OnFeatureClick {
        void onFeatureClick(FeatureItem item);
    }

    private final List<FeatureItem> items;
    private final OnFeatureClick listener;

    public FeatureAdapter(List<FeatureItem> items, OnFeatureClick listener) {
        this.items = items;
        this.listener = listener;
    }

    @NonNull
    @Override
    public Holder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return new Holder(ItemFeatureBinding.inflate(LayoutInflater.from(parent.getContext()), parent, false));
    }

    @Override
    public void onBindViewHolder(@NonNull Holder holder, int position) {
        FeatureItem item = items.get(position);
        ItemFeatureBinding b = holder.binding;
        b.featureTitle.setText(item.title);
        b.featureBlurb.setText(item.blurb);
        b.featureImage.setImageResource(item.imageRes);
        b.getRoot().setOnClickListener(v -> listener.onFeatureClick(item));
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    static class Holder extends RecyclerView.ViewHolder {
        final ItemFeatureBinding binding;

        Holder(ItemFeatureBinding binding) {
            super(binding.getRoot());
            this.binding = binding;
        }
    }
}
