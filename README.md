# Blender Test Project

This repository contains a Blender Python script that creates a mechanical piston assembly similar to the aged animatronic mechanisms found in 1980s-era theme parks. The script builds geometry, applies procedural rusty materials, sets up dim lighting and a basic camera, then animates the piston with jerky servo-like motion.

## Files

- `piston_anim.py` – Python script for Blender. Run this inside Blender's scripting workspace or from the command line with `blender --python piston_anim.py` to generate the scene and animation.

## Usage

1. Open Blender (version 3.x or newer recommended).
2. Load `piston_anim.py` in the text editor and press **Run Script**.
3. The piston assembly and animation will be created automatically.
4. Optionally supply your own servo audio by editing the commented section near the bottom of the script.
5. Use Cycles to render the animation frames.

The lighting simulates a dim backstage bulb and the animation includes random jitter to imitate worn mechanical parts. Adjust the materials or keyframes as desired to refine the look.
