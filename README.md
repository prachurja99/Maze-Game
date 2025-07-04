# Beat the Maze !  🌀

Collect hidden gold, out‑smart roaming enemies, and beat the clock  
— a 2‑D maze adventure built entirely with **Python + OpenGL** as part of **CSE 423 (Computer Graphics)** at **BRAC University**.

<p align="center">
  <img src="assets/demo.gif" alt="Gameplay demo" width="640"/>
</p>

---

## Table of Contents
1. [Key Features](#key-features)
2. [Gameplay & Controls](#gameplay--controls)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)

---

## Key Features
- **Pure OpenGL drawing** – Mid‑point line & circle algorithms (no sprites/bitmaps).
- **Dual tools** – *Drill* (rapid bullets) & *Hammer* (AoE bomb) toggle with `T`.
- **Randomised levels** – Enemies × 5 and gold × 7 spawn uniquely each run.
- **Score, timer, lives** – Extra time every 30 pts; three lives to clear the maze.
- **Mouse‑driven UI** – Pause/Play, Restart, and Quit icons built from primitives.
- Lightweight: a single `Maze Game.py` (~500 lines) + optional images/GIFs only.

---

## Gameplay & Controls
| Action | Key / Mouse |
|--------|-------------|
| Move                   | **Arrow Keys** |
| Toggle Drill ↔ Hammer  | **T** |
| Shoot (Drill mode)     | **W A S D** |
| Pause / Resume         | **Click** the Pause▐▌ icon (top‑right) |
| Restart                | **Click** the Back↩ icon (top‑left) |
| Quit                   | **Click** the X icon (top‑right) |

### Objective
1. **Hammer mode** to break bricks, grab all 7 hidden gold bars.  
2. Avoid or destroy enemies; each enemy is worth 10 pts.  
3. Finish before the 45 s timer hits zero (earn +10 s per 30 pts).

---

## Prerequisites
| Dependency            | Windows / macOS (pip)                       | Ubuntu / Debian‑based (apt) |
|-----------------------|---------------------------------------------|-----------------------------|
| Python ≥ 3.9          | <https://python.org>                        | `sudo apt install python3` |
| PyOpenGL (+Accelerate)| `pip install PyOpenGL PyOpenGL_accelerate`  | same `pip` command |
| FreeGLUT runtime      | Bundled DLL / Homebrew `brew install freeglut` | `sudo apt install freeglut3‑dev` |

> **Tip:** installing `PyOpenGL_accelerate` is optional but boosts performance.

---

## Installation
```bash
# 1. Clone the repository
git clone https://github.com/prachurja99/Maze-Game.git
cd Maze-Game

# 2. (Recommended) activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt     # or run the pip commands above
