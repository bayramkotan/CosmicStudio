# 🌟 CosmicStudio

### *Watch Stars Being Born, Live, and Die — All in Your Computer*

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)
![Stars](https://img.shields.io/github/stars/bayramkotan/CosmicStudio?style=social)

**An interactive journey through the cosmos — from stellar birth to spectacular death**

[Features](#-features) • [Installation](#-installation) • [Physics](#-the-physics) • [Gallery](#-gallery) • [Roadmap](#-roadmap)

</div>

---

## 🎯 What is CosmicStudio?

CosmicStudio brings the universe to your desktop. Using **real stellar physics equations**, it simulates the complete life cycle of stars — from their fiery birth in cosmic nurseries to their final fate as white dwarfs, neutron stars, or black holes.

**This isn't a simple animation.** Every point on the H-R diagram is calculated using the same equations astrophysicists use to understand stars. Every color change reflects real temperature variations. Every phase transition follows the laws of nuclear physics.

### Why CosmicStudio?

- 🔬 **Real Physics**: Solves actual stellar structure equations (mass, pressure, energy, temperature)
- 🎨 **Beautiful Visualization**: Modern UI with interactive H-R diagrams and 3D-style star cross-sections
- ⚡ **Real-Time**: Watch billions of years unfold in minutes
- 📚 **Educational**: Perfect for students, educators, and space enthusiasts
- 🚀 **Fast**: Optimized calculations, smooth 20 FPS animations

---

## ✨ Features

### 🌌 The Stellar Evolution Engine

The heart of CosmicStudio is a sophisticated physics engine that models stars through their entire lives:

**Nuclear Fusion Reactions:**
- **PP-Chain**: Powers Sun-like stars (converts Hydrogen → Helium)
- **CNO Cycle**: Dominates in massive stars
- **Triple-Alpha**: Helium burning in red giants (creates Carbon)

**Evolutionary Phases:**
```
Birth → Main Sequence → Red Giant → Final Fate
  ↓         ↓              ↓            ↓
ZAMS    (90% of life)   Expansion   WD/NS/BH
```

**Complete Evolution Tracks:**
- ⭐ **Low-Mass Stars** (< 0.5 M☉): Trillion-year lifespans, gentle white dwarf deaths
- 🌟 **Sun-like Stars** (0.5-8 M☉): Billions of years, planetary nebula finale
- 💥 **Massive Stars** (> 8 M☉): Brief but brilliant, ending in supernovae

### 📊 Interactive Hertzsprung-Russell Diagram

The H-R diagram is astronomy's most important tool — and ours is gorgeous:

- **Evolution Track**: Watch your star's journey across the diagram
- **Spectral Classes**: Color-coded regions (O, B, A, F, G, K, M)
- **Reference Lines**: Main sequence, constant radius curves
- **Live Cursor**: Yellow star shows current evolutionary state
- **Zoom & Pan**: Explore specific regions in detail

*Temperature (x-axis) vs Luminosity (y-axis) — the story of every star ever born*

### 🎨 Star Cross-Section Visualization

See inside a star! Real-time visualization of internal structure:

- **Core** (White/Yellow): Nuclear fusion furnace, millions of degrees
- **Radiative Zone** (Orange): Energy flows outward as photons
- **Convective Zone** (Red): Bubbling plasma carries heat to surface
- **Photosphere** (Color-coded): What you'd see from space

Each layer's size and color adjusts based on the star's mass and age!

### 🎮 Intuitive Controls

**Mass Selection:**
- Continuous range: 0.1 to 100 solar masses
- Quick presets: 0.5 M☉ (Red Dwarf), 1.0 M☉ (Sun), 5.0 M☉ (Blue Star), 20 M☉ (Supergiant)

**Time Navigation:**
- Slider spans entire stellar lifetime
- Play/Pause animations
- Jump to any evolutionary phase instantly

**Real-Time Display:**
- Current phase name
- Mass, radius, luminosity
- Surface temperature & spectral class
- Internal composition (H, He, metals)

---

## 🚀 Installation

### Quick Start (Recommended)

**Linux/Mac:**
```bash
git clone https://github.com/bayramkotan/CosmicStudio.git
cd CosmicStudio
./run.sh
```

**Windows:**
```batch
git clone https://github.com/bayramkotan/CosmicStudio.git
cd CosmicStudio
run.bat
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/bayramkotan/CosmicStudio.git
cd CosmicStudio

# Install dependencies
pip install -r requirements.txt

# Launch!
cd src
python main.py
```

**Requirements:**
- Python 3.8+
- PySide6 (modern Qt6 GUI)
- NumPy (fast numerical arrays)
- SciPy (ODE solver)
- Matplotlib (scientific plotting)

---

## 🔬 The Physics

### The Four Fundamental Equations

CosmicStudio solves the stellar structure equations that govern all stars:

**1. Mass Conservation** — *How mass distributes inside the star*
```
dM(r)/dr = 4πr²ρ(r)
```

**2. Hydrostatic Equilibrium** — *Balance between gravity and pressure*
```
dP(r)/dr = -GMρ/r²
```

**3. Energy Generation** — *Nuclear fusion power output*
```
dL(r)/dr = 4πr²ρε(ρ,T)
```

**4. Energy Transport** — *How heat flows from core to surface*
```
dT/dr = -(3κρL)/(16πacT³r²)  [Radiative]
dT/dr = Adiabatic Gradient      [Convective]
```

### Stellar Life Cycles

#### 🔴 Low-Mass Stars (< 0.5 M☉) — *The Eternal Ones*
- **Lifetime**: > 100 billion years (longer than universe age!)
- **Fate**: Slow fade to white dwarf
- **Example**: Proxima Centauri

#### 🟡 Sun-like Stars (0.5 - 8 M☉) — *The Planetary Nebula Makers*
```
Main Sequence (10 Gyr) → Red Giant (1 Gyr) → Planetary Nebula → White Dwarf
```
- **Lifetime**: 500 million to 50 billion years
- **Fate**: Beautiful planetary nebula, then white dwarf
- **Example**: Our Sun (currently mid-life)

#### 🔵 Massive Stars (8 - 25 M☉) — *The Supernovae*
```
Main Sequence (10 Myr) → Supergiant (1 Myr) → SUPERNOVA! → Neutron Star
```
- **Lifetime**: 10-100 million years
- **Fate**: Spectacular supernova explosion
- **Example**: Betelgeuse (will explode "soon")

#### ⚫ Super-Massive Stars (> 25 M☉) — *The Black Hole Factories*
```
Main Sequence (3 Myr) → Hypergiant → HYPERNOVA! → Black Hole
```
- **Lifetime**: < 10 million years
- **Fate**: Collapse into black hole
- **Example**: Eta Carinae

### Temperature-Color Connection

Ever wonder why stars have different colors?

| Temperature | Color | Spectral Type | Example |
|------------|-------|---------------|---------|
| 40,000 K | Electric Blue | O | Mintaka (Orion's Belt) |
| 20,000 K | Blue-White | B | Rigel |
| 10,000 K | White | A | Sirius |
| 7,500 K | Yellow-White | F | Procyon |
| 6,000 K | Yellow | G | **The Sun** |
| 4,000 K | Orange | K | Arcturus |
| 3,000 K | Red | M | Betelgeuse |

*CosmicStudio calculates these colors using blackbody radiation physics!*

---

## 📸 Gallery

### The Sun's Future
*Watch our Sun swell into a red giant in 5 billion years, then shrink to a white dwarf*

### Supernova in Action
*See a 20 M☉ star race through its life and explode spectacularly*

### The Main Sequence
*The cosmic highway where stars spend 90% of their lives*

---

## 🎓 Educational Use

Perfect for:
- **University Courses**: Astrophysics, Astronomy 101-400 level
- **High School**: AP Physics, Advanced Astronomy
- **Planetariums**: Interactive public demonstrations
- **Self-Study**: Understanding stellar evolution deeply

**Learning Outcomes:**
- ✅ Understand the H-R diagram intuitively
- ✅ See how mass determines stellar fate
- ✅ Grasp nuclear fusion processes
- ✅ Visualize billion-year timescales
- ✅ Connect theory to real stars in the night sky

---

## 🛠️ Technical Architecture

```
CosmicStudio/
├── physics/              # The brain — stellar evolution engine
│   ├── stellar_constants.py      # Universal physical constants
│   ├── stellar_equations.py      # Core physics equations
│   └── stellar_evolution.py      # Evolution calculator
├── ui/                   # The face — beautiful visualizations
│   ├── main_window.py            # Application shell
│   ├── hr_diagram_widget.py      # H-R diagram (Matplotlib)
│   ├── star_cross_section_widget.py  # Star interior view
│   └── control_panel.py          # User controls
└── resources/            # Presets and scenarios
```

**Design Philosophy:**
- Physics engine completely separate from UI (testable, reusable)
- Modern PySide6 for cross-platform compatibility
- Matplotlib for publication-quality plots
- Custom Qt painting for star visualization

---

## 🗺️ Roadmap

### Coming Soon
- [ ] **Binary Star Systems**: Watch stars orbit and exchange mass
- [ ] **Custom Composition**: Vary metallicity (X, Y, Z sliders)
- [ ] **Stellar Rotation**: See how spin affects evolution
- [ ] **Mass Loss Winds**: Model realistic stellar winds
- [ ] **Nucleosynthesis View**: Track element production (C, O, Fe...)

### Future Vision
- [ ] **Video Export**: Create time-lapse animations
- [ ] **Multi-Star Comparison**: Compare 2-4 tracks simultaneously
- [ ] **Web Version**: Browser-based using PyScript/WASM
- [ ] **VR Mode**: Immersive stellar exploration

---

## 🤝 Contributing

Love astrophysics? Want to improve CosmicStudio?

**We need:**
- 🔬 Physics improvements (better opacity models, rotation)
- 🎨 UI enhancements (themes, layouts)
- 📚 Documentation (tutorials, videos)
- 🐛 Bug reports and fixes
- 🌍 Translations (Turkish, Spanish, French...)

```bash
# Fork the repo
git clone https://github.com/bayramkotan/CosmicStudio.git
cd CosmicStudio

# Create feature branch
git checkout -b amazing-feature

# Make changes, commit, push
git push origin amazing-feature

# Open Pull Request on GitHub!
```

---

## 📚 References & Inspiration

**Textbooks:**
- Kippenhahn, Weigert & Weiss — *"Stellar Structure and Evolution"* (The Bible)
- Phillips — *"The Physics of Stars"*
- LeBlanc — *"An Introduction to Stellar Astrophysics"*

**Professional Codes:**
- **MESA**: Industry-standard stellar evolution (messier but complete)
- **STARS**: Cambridge stellar models
- **Geneva Models**: Rotating star evolution

**Standing on the Shoulders of Giants:**
- Hertzsprung & Russell (1911-1913): The H-R diagram
- Eddington (1920s): Interior structure theory
- Bethe (1939): Nuclear fusion in stars (Nobel Prize)
- Schwarzschild (1906-1979): Stellar structure equations

---

## ⚖️ License

**MIT License** — Free for everyone, forever.

Use it for homework, teaching, research, fun — whatever you want!

---

## 👨‍💻 Author

**Bayram Kotan**

PhD Candidate | Data & Cloud Architect | Astrophysics Enthusiast

[GitHub](https://github.com/bayramkotan) • [CosmicStudio](https://github.com/bayramkotan/CosmicStudio)

---

<div align="center">

### ⭐ If you enjoyed CosmicStudio, give it a star!

*Made with ❤️ for everyone who's ever looked up at the night sky and wondered...*

**"What are stars made of? How do they shine? How do they die?"**

*Now you can find out.*

</div>
