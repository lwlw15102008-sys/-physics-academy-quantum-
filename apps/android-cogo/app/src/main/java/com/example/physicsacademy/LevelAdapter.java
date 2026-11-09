package com.example.physicsacademy;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.physicsacademy.databinding.ItemLevelBinding;

public class LevelAdapter extends RecyclerView.Adapter<LevelAdapter.Holder> {
    private final int[] images;
    private final String[] names;

    public LevelAdapter(int[] images, String[] names) {
        this.images = images;
        this.names = names;
    }

    @NonNull
    @Override
    public Holder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return new Holder(ItemLevelBinding.inflate(LayoutInflater.from(parent.getContext()), parent, false));
    }

    @Override
    public void onBindViewHolder(@NonNull Holder holder, int position) {
        ItemLevelBinding b = holder.binding;
        int level = position + 1;
        b.levelImage.setImageResource(images[position]);
        b.levelImage.setContentDescription(b.getRoot().getContext().getString(R.string.level_content_desc, level, names[position]));
        b.levelNumber.setText(b.getRoot().getContext().getString(R.string.level_label, level));
        b.levelName.setText(names[position]);
    }

    @Override
    public int getItemCount() {
        return Math.min(images.length, names.length);
    }

    static class Holder extends RecyclerView.ViewHolder {
        final ItemLevelBinding binding;

        Holder(ItemLevelBinding binding) {
            super(binding.getRoot());
            this.binding = binding;
        }
    }
}
