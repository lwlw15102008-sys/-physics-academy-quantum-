package com.example.physicsacademy;

import android.os.Bundle;
import android.view.View;

import androidx.annotation.IdRes;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.fragment.app.Fragment;

import com.example.physicsacademy.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {
    private ActivityMainBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // The app is Arabic-first: force right-to-left whatever the device language is.
        getWindow().getDecorView().setLayoutDirection(View.LAYOUT_DIRECTION_RTL);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // Keep content clear of the system bars (edge-to-edge is enforced on API 35+)
        ViewCompat.setOnApplyWindowInsetsListener(binding.getRoot(), (v, insets) -> {
            Insets bars = insets.getInsets(
                    WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout());
            v.setPadding(bars.left, bars.top, bars.right, bars.bottom);
            return insets;
        });

        binding.bottomNav.setOnItemSelectedListener(item -> {
            show(item.getItemId());
            return true;
        });

        // On rotation the FragmentManager restores the visible fragment, so only select on first launch.
        if (savedInstanceState == null) {
            binding.bottomNav.setSelectedItemId(R.id.nav_home);
        }
    }

    /** Switches to a bottom-navigation tab (used by the "Start learning" button). */
    public void openTab(@IdRes int tabId) {
        binding.bottomNav.setSelectedItemId(tabId);
    }

    private void show(@IdRes int tabId) {
        Fragment fragment;
        if (tabId == R.id.nav_home) {
            fragment = new HomeFragment();
        } else if (tabId == R.id.nav_learn) {
            fragment = new LearnFragment();
        } else if (tabId == R.id.nav_labs) {
            fragment = FeatureListFragment.labs();
        } else if (tabId == R.id.nav_games) {
            fragment = FeatureListFragment.games();
        } else {
            fragment = new ProgressFragment();
        }
        getSupportFragmentManager().beginTransaction().replace(R.id.container, fragment).commit();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        this.binding = null;
    }
}
