# CosmicStudio - Stellar Evolution Simulator

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)

**CosmicStudio** is an interactive stellar evolution simulator that visualizes the life cycle of stars using real stellar physics equations.

![CosmicStudio Screenshot](docs/screenshot.png)

## Features

### 🌟 Stellar Physics Engine
- **Full Stellar Structure Equations**: Mass conservation, hydrostatic equilibrium, energy generation, and energy transport
- **Nuclear Reactions**: PP-chain, CNO cycle, and triple-alpha process
- **Realistic Evolution Phases**: 
  - Pre-Main Sequence
  - Main Sequence (ZAMS to TAMS)
  - Red Giant Branch
  - Horizontal Branch
  - Asymptotic Giant Branch
  - White Dwarf / Neutron Star / Black Hole

### 📊 Interactive Visualizations
- **Hertzsprung-Russell (H-R) Diagram**: 
  - Shows stellar evolution track
  - Spectral class regions (O, B, A, F, G, K, M)
  - Constant radius lines
  - Real-time position marker
  
- **Star Cross Section View**:
  - Internal structure (core, radiative zone, convective zone)
  - Real-time color based on temperature
  - Detailed parameter display

### 🎮 User Controls
- **Mass Range**: 0.1 to 100 solar masses
- **Preset Configurations**: Quick access to common stellar types
- **Playback Controls**: Play, pause, and reset evolution
- **Time Slider**: Navigate through billions of years of evolution

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
cd CosmicStudio
pip install -r requirements.txt
```

### Run the Application

```bash
cd src
python main.py
```

## Usage

### Quick Start

1. **Select Stellar Mass**: Use the mass spinner or preset buttons (0.5, 1.0, 5.0, 20 M☉)
2. **View Evolution**: The H-R diagram shows the complete evolutionary track
3. **Navigate Time**: Use the time slider to explore different evolutionary phases
4. **Play Animation**: Click "Play" to watch the star evolve in real-time
5. **Examine Structure**: The cross-section view shows internal layers

### Understanding the Displays

#### H-R Diagram
- **X-axis**: log₁₀(Temperature) - hotter stars on the left
- **Y-axis**: log₁₀(Luminosity) - brighter stars at the top
- **Green circle**: Zero Age Main Sequence (ZAMS)
- **Red square**: Final evolutionary state
- **Yellow star**: Current position

#### Star Cross Section
- **Core**: Nuclear fusion region (white/yellow)
- **Radiative Zone**: Energy transport via photons (orange)
- **Convective Zone**: Energy transport via convection (red-orange)
- **Surface**: Photosphere (color based on temperature)

### Keyboard Shortcuts

- `Ctrl+S`: Export evolution track to JSON
- `Ctrl+0`: Reset H-R diagram zoom
- `Ctrl+Q`: Quit application

## Physics Background

### Stellar Structure Equations

The simulator solves the four fundamental differential equations:

1. **Mass Conservation**:
   ```
   dM(r)/dr = 4πr²ρ(r)
   ```

2. **Hydrostatic Equilibrium**:
   ```
   dP(r)/dr = -GMρ/r²
   ```

3. **Energy Generation**:
   ```
   dL(r)/dr = 4πr²ρε(ρ,T)
   ```

4. **Energy Transport** (Radiative):
   ```
   dT/dr = -(3κρL)/(16πacT³r²)
   ```

### Nuclear Energy Sources

- **PP Chain** (T > 4×10⁶ K): Hydrogen → Helium in low-mass stars
- **CNO Cycle** (T > 1.3×10⁷ K): Hydrogen → Helium in massive stars
- **Triple-Alpha** (T > 10⁸ K): Helium → Carbon in giants

### Evolution Phases

#### Low-Mass Stars (< 0.5 M☉)
- Extremely long main sequence lifetimes (> age of universe)
- Evolve directly to white dwarfs

#### Intermediate-Mass Stars (0.5 - 8 M☉)
1. Main Sequence (H burning)
2. Subgiant (H-shell burning)
3. Red Giant Branch (expanding envelope)
4. Horizontal Branch (He burning core)
5. Asymptotic Giant Branch (double-shell burning)
6. Planetary Nebula ejection
7. White Dwarf remnant

#### High-Mass Stars (> 8 M☉)
1. Main Sequence (rapid H burning)
2. Red Supergiant (massive expansion)
3. Core collapse
4. Supernova explosion
5. Neutron Star (8-25 M☉) or Black Hole (> 25 M☉)

## Technical Details

### Architecture

```
CosmicStudio/
├── src/
│   ├── main.py                          # Application entry point
│   ├── physics/                         # Physics engine
│   │   ├── stellar_constants.py         # Physical constants
│   │   ├── stellar_equations.py         # Fundamental equations
│   │   └── stellar_evolution.py         # Evolution calculator
│   └── ui/                              # User interface
│       ├── main_window.py               # Main window
│       ├── hr_diagram_widget.py         # H-R diagram
│       ├── star_cross_section_widget.py # Star visualization
│       └── control_panel.py             # User controls
```

### Dependencies

- **PySide6**: Modern Qt6 bindings for GUI
- **NumPy**: Numerical computations
- **SciPy**: ODE solver for stellar structure
- **Matplotlib**: Scientific plotting for H-R diagram

## Roadmap

### Planned Features

- [ ] Custom composition (X, Y, Z) controls
- [ ] Binary star systems
- [ ] Stellar rotation effects
- [ ] Mass loss and stellar winds
- [ ] Nucleosynthesis visualization
- [ ] Export to animation/video
- [ ] Multiple comparison tracks
- [ ] Full numerical integration mode
- [ ] WebGL version for browser

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/CosmicStudio.git
cd CosmicStudio

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

## References

### Books
- **"An Introduction to Stellar Astrophysics"** - Francis LeBlanc
- **"Stellar Structure and Evolution"** - Kippenhahn, Weigert & Weiss
- **"The Physics of Stars"** - A.C. Phillips

### Software
- **MESA** (Modules for Experiments in Stellar Astrophysics)
- **EZ-Web** (Easy Evolution and ZAMS)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Bayram**
- PhD Candidate in Data Science & Machine Learning
- Data & Cloud Architect
- [GitHub](https://github.com/yourusername)
- [LinkedIn](https://linkedin.com/in/yourprofile)

## Acknowledgments

- Stellar physics equations based on standard stellar structure theory
- H-R diagram concept from Hertzsprung and Russell (1911-1913)
- Color-temperature mapping from blackbody radiation theory
- Inspired by professional stellar evolution codes like MESA

---

**Note**: This is a simplified stellar evolution model designed for educational and visualization purposes. For research-grade stellar evolution calculations, please use professional codes like MESA, STARS, or Geneva evolution models.
