# RingLight

Simple on-screen ringlight overlay written in PyQt5.

Usage
-----

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install PyQt5
```

3. Run the app (from the project root):

```bash
source .venv/bin/activate
python main.py
```

Notes about Wayland/X11
-----------------------
- If you're on Wayland (Gnome), Qt may prefer X11. To force Wayland set:

```bash
QT_QPA_PLATFORM=wayland source .venv/bin/activate && python main.py
```

Controls (in-app)
------------------
The floating control panel appears at the bottom-center of the screen and contains exactly three sliders stacked vertically (no labels):

- Top slider — Brightness (0..255)
- Middle slider — Thickness (30..140)
- Bottom slider — Light type (integer index)
  - 0 = White
  - 1 = Natural
  - 2 = Warm
  - 3 = Soft

Behavior
--------
- The overlay is frameless, stays on top, and is transparent to clicks so you can interact with underlying applications.
- Use the sliders to adjust the overlay in real time.
- To quit, close the terminal running the app (Ctrl+C) or kill the process.

Troubleshooting
---------------
- If the control panel doesn't appear, verify `PyQt5` is installed in the active environment.
- If the overlay or controls won't accept input on Wayland, try the `QT_QPA_PLATFORM=wayland` environment variable, or run under X11.

Development notes
-----------------
- Main code is in `main.py`.
- The control panel syncs slider values with the overlay at runtime.

License
-------
- (No license specified.)
