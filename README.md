# GCode 3DP Layer Remover

It is a Python program to cut the bottom and top layers of the gcode in a FDM process, why? Because i needed to show the infill and shells in 3D printing courses

<img src="/img/img1.png" width="700">

In the current state, you need:

- Python 3 to run the code
- Write manually the name of your file in the code, layer where the fan works at 100% and how many layers to remove from top and bottom.
- Put the .gcode in the same folder as the program
- The original .gcode must include raft, as the infill does not stick firmly to the platform

I have only tried cubes in my Ender 3.

Further work:

- Adapt to first layer settings (speeds, temps)
- Make a UI

This repository includes an example of a 20x20 cube, the original and modified file.


