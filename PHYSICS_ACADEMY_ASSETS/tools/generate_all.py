#!/usr/bin/env python3
"""Regenerates every procedural asset. Usage: python3 PHYSICS_ACADEMY_ASSETS/tools/generate_all.py"""
import os, sys, importlib.util
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import gen_icons, gen_scenes, gen_objects, gen_mascot, gen_glb
spec = importlib.util.spec_from_file_location("gen_base", os.path.join(here, "generate_assets.py")); base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
if __name__ == "__main__":
    base.make_logo(); base.make_backgrounds()
    for i in range(15): base.badge(i)
    src = base.out("08_UI_ILLUSTRATIONS/quantum-dashboard-concept.png")
    if os.path.exists(src): base.Image.open(src).convert("RGB").save(base.out("08_UI_ILLUSTRATIONS/quantum-dashboard-concept.webp"), quality=82, method=6)
    print("icons", gen_icons.run(), "| scenes", gen_scenes.run(), "| objects", gen_objects.run(), "| mascot", gen_mascot.run(), "| glb", len(gen_glb.run()))
